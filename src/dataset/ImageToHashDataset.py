import multiprocessing
import os

import imagehash
import pandas as pd
from PIL import Image
from tqdm import tqdm


class ImageToHashDataset(object):

    def __init__(self, img_file_list, hash_size=16, verbose=0):

        self.img_file_list = img_file_list
        self.hash_size = hash_size
        self.verbose = verbose
        self.df_dataset = None

    @staticmethod
    def img_hash(image_path, hash_size):
        """

        Perceptual Hash computation.

        Implementation follows http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.htm

        :param image_path: A filename (string).
        :param hash_size: The size of hash.
        :return: an ImageHash.
        """
        return imagehash.phash(Image.open(image_path), hash_size=hash_size)

    def build_dataset(self, parallel=False, batch_size=32):
        """
        Build the dataset.
        """

        print('Building the dataset...')

        if parallel:
            print('\tParallel mode has been enabled...')
            number_of_cpu = multiprocessing.cpu_count()
            print("CPU: {}".format(number_of_cpu))

            if number_of_cpu >= 2:
                self.number_of_cpu = number_of_cpu
            else:
                raise ValueError("Number of CPU must greater than or equal to 2.")
            df_hashes = self.parallel_build_hash_to_image_dataframe(batch_size=batch_size)
        else:
            df_hashes = self.build_hash_to_image_dataframe()

        df_hashes = df_hashes[['file', 'short_file', 'hash', 'hash_list']]
        lambdafunc = lambda x: pd.Series([int(i, 16) for key, i in zip(range(0, len(x['hash_list'])), x['hash_list'])])
        newcols = df_hashes.apply(lambdafunc, axis=1)
        newcols.columns = [str(i) for i in range(0, len(df_hashes.iloc[0]['hash_list']))]

        # df_dataset's columns: 'file', 'hash', 'hash_list', '0', '1', '2', ..., 'N'
        self.df_dataset = df_hashes.join(newcols)
        return self.df_dataset

    def build_hash_to_image_dataframe(self):
        """
        For each image calculate the phash and store it in a Pandas DataFrame.

        :return: a Pandas DataFrame with columns:
        - file(image's file path)
        - hash(hash code associated to image),
        - hash_list(list of all hash code's elements)
        """

        # df_hashes's columns: file, hash, hash_list
        # file -> image's file path
        # hash -> hash code associated to image
        # hash_list -> list of all hash code's elements
        df_hashes = pd.DataFrame()
        already_exist_counter = 0
        # hash code -> image's file path
        dict_hash_to_images = {}

        # For each image calculate the phash and store it in a DataFrame
        for image in tqdm(self.img_file_list):

            hash_code = self.img_hash(image, self.hash_size)

            result = {'file': image, 'short_file': image.split(os.sep)[-1], 'hash': hash_code,
                      'hash_list': list(str(hash_code))}
            df_hashes = df_hashes.append(result, ignore_index=True)

            if hash_code in dict_hash_to_images:
                if self.verbose == 2:
                    print(image, '  already exists as', ' '.join(dict_hash_to_images[hash_code]))
                already_exist_counter += 1

            dict_hash_to_images[hash_code] = dict_hash_to_images.get(hash_code, []) + [image]

        # Are there any duplicates in terms of hashes of size 'hash_size'?
        print("{0} out to {1}".format(already_exist_counter, len(self.img_file_list)))
        # TODO warning
        # assert already_exist_counter == 0, "it actually can only represent 16^" + str(self.hash_size) + \
        #                                  " values let's try with a bigger hash."

        return df_hashes

    def multiprocessing_img_hash(self, block):
        """
        Hash a block of images.
        :param block: a block containing the path of images.
        :return: a dict containing the corresponding hashes.
        """

        result = {}

        for i, image in tqdm(enumerate(block)):
            hash_code = self.img_hash(image, self.hash_size)
            result['file'] = result.get('file', []) + [image]
            result['short_file'] = result.get('short_file', []) + [image.split(os.sep)[-1]]
            result['hash'] = result.get('hash', []) + [hash_code]
            result['hash_list'] = result.get('hash_list', []) + [list(str(hash_code))]

        return result

    def parallel_build_hash_to_image_dataframe(self, batch_size):
        """
        For each image calculate the phash and store it in a Pandas DataFrame.

        :return: a Pandas DataFrame with columns:
        - file(image's file path)
        - hash(hash code associated to image),
        - hash_list(list of all hash code's elements)
        """
        df_hashes = pd.DataFrame()

        result_list = []
        # initialise the pool outside the loop
        pool = multiprocessing.Pool(processes=self.number_of_cpu)
        # For each image calculate the phash and store it in a DataFrame
        for i in tqdm(range(0, len(self.img_file_list), batch_size)):
            # delegate work inside the loop
            r = pool.apply_async(self.multiprocessing_img_hash, args=(self.img_file_list[i:i + batch_size],))
            result_list.append(r)

        # shut down the pool
        pool.close()
        pool.join()

        # get the results
        for i, sublist in tqdm(enumerate(result_list)):
            row = sublist.get()
            if i == 0:
                df_hashes = pd.DataFrame(row)
            else:
                temp = pd.DataFrame(row)
                df_hashes = df_hashes.append(temp, ignore_index=True)

        return df_hashes
