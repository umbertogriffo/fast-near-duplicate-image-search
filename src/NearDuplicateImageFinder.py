import multiprocessing
import os
import sys
import time

import imagehash
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.neighbors import KDTree
from tqdm import tqdm

from utils.ImgUtils import ImgUtils


class NearDuplicateImageFinder(object):

    def __init__(self, img_file_list, hash_size=16, parallel=False, batch_size=32, verbose=0):

        self.img_file_list = img_file_list
        self.hash_size = hash_size
        self.parallel = parallel
        self.batch_size = batch_size
        self.verbose = verbose

        self.df_dataset = None
        self.tree = None

        if self.parallel:
            number_of_cpu = multiprocessing.cpu_count()
            print("CPU: {}".format(number_of_cpu))

            if number_of_cpu >= 2:
                self.number_of_cpu = number_of_cpu
            else:
                raise ValueError("Number of CPU must greater than or equal to 2.")

        self.build_dataset()
        self.build_tree()

    @staticmethod
    def _getThreads():
        """ Returns the number of available threads on a posix/win based system """
        if sys.platform == 'win32':
            return (int)(os.environ['NUMBER_OF_PROCESSORS'])
        else:
            return (int)(os.popen('grep -c cores /proc/cpuinfo').read())

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

            result = {'file': image, 'hash': hash_code, 'hash_list': list(str(hash_code))}
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

        for i, image in enumerate(block):
            hash_code = self.img_hash(image, self.hash_size)
            result['file'] = result.get('file', []) + [image]
            result['hash'] = result.get('hash', []) + [hash_code]
            result['hash_list'] = result.get('hash_list', []) + [list(str(hash_code))]

        return result

    def parallel_build_hash_to_image_dataframe(self):
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
        for i in range(0, len(self.img_file_list), self.batch_size):
            # delegate work inside the loop
            r = pool.apply_async(self.multiprocessing_img_hash, args=(self.img_file_list[i:i + self.batch_size],))
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

    def build_dataset(self):
        """
        Build the dataset for the KDTree.
        """

        print('Building the dataset...')

        if self.parallel:
            print('\tParallel mode has been enabled...')
            df_hashes = self.parallel_build_hash_to_image_dataframe()
        else:
            df_hashes = self.build_hash_to_image_dataframe()

        df_hashes = df_hashes[['file', 'hash', 'hash_list']]
        lambdafunc = lambda x: pd.Series([int(i, 16) for key, i in zip(range(0, len(x['hash_list'])), x['hash_list'])])
        newcols = df_hashes.apply(lambdafunc, axis=1)
        newcols.columns = [str(i) for i in range(0, len(df_hashes.iloc[0]['hash_list']))]

        # df_dataset's columns: 'file', 'hash', 'hash_list', '0', '1', '2', ..., 'N'
        self.df_dataset = df_hashes.join(newcols)

    def build_tree(self):

        print('Building the KDTree...')

        hash_str_len = len(self.df_dataset.at[0, 'hash_list'])
        self.tree = KDTree(self.df_dataset[[str(i) for i in range(0, hash_str_len)]], metric='manhattan')

    def find_duplicates(self, nearest_neighbors=10, threshold=150):
        """
        Find similar images.
        :param nearest_neighbors:
        :param threshold:
        :return: files_to_keep, files_to_remove, dict_image_to_duplicates
        """

        print('Finding duplicates...')
        start_time = time.time()

        dict_image_to_duplicates = dict()
        keep = []
        remove = []
        hash_str_len = len(self.df_dataset.at[0, 'hash_list'])
        # 'distances' is a matrix NxM where N is the number of images and M is the value of nearest_neighbors_in.
        # For each image it contains an array containing the distances of k-nearest neighbors.
        # 'indices' is a matrix NxM where N is the number of images and M is the value of nearest_neighbors_in.
        # For each image it contains an array containing the indices of k-nearest neighbors.
        distances, indices = self.tree.query(self.df_dataset[[str(i) for i in range(0, hash_str_len)]],
                                             k=nearest_neighbors)
        max_distance = distances.max()
        print("\t Max distance: {}".format(max_distance))
        min_distance = distances.min()
        print("\t Min distance: {}".format(min_distance))
        # Find the indices of distances elements that are non-zero and less or equal to threshold_in.
        above_threshold_idx = np.argwhere((distances <= threshold) & (distances > 0))

        pairs_of_indexes_of_duplicate_images = set([tuple(sorted([indices[idx[0], 0], indices[idx[0], idx[1]]]))
                                                    for idx in above_threshold_idx])

        # (129, 162), (176, 358), (185, 266), (129, 236), (19, 381), (60, 253), (153, 415), (20, 223), (188, 329),
        # (31, 269), (66, 214), (168, 274), (119, 250), (231, 255), (230, 250), (141, 277), (311, 388), (129, 311)
        # 129 -> 162, 236, 311

        pair_sorted_by_first = sorted(list(pairs_of_indexes_of_duplicate_images), key=lambda tup: tup[0])
        # [..., (129, 162), (129, 236), (129, 311), (129, 171), ...]

        [dict_image_to_duplicates[t[0]].append(t[1]) if t[0] in list(dict_image_to_duplicates.keys())
         else dict_image_to_duplicates.update({t[0]: [t[1]]}) for t in pair_sorted_by_first]
        # {... , 129: [162, 236, 311, 171], ... }

        # dict_image_to_duplicates:
        # A -> C,D
        # B -> E,F,C
        # D -> A
        # C -> A,B,D
        # M -> N,O
        # Results:
        # key       keep        remove
        # A         A           C,D
        # B         A,B         C,D,E,F
        # D         A,B         C,D,E,F
        # C         A,B         C,D,E,F
        # M         A,B,M       C,D,E,F,N,O
        for k, (key, value) in enumerate(dict_image_to_duplicates.items()):
            if k == 0:
                keep.append(key)
                remove.extend(value)
            else:
                if key not in remove:
                    keep.append(key)
                    remove.extend(list(set(value).difference(set(remove))))

        files_to_remove = [f for f in list(self.df_dataset.iloc[remove]['file'])]
        print("\t number of files to remove: {}".format(len(files_to_remove)))

        files_to_keep = [f for f in list(self.df_dataset.iloc[keep]['file'])]
        print("\t number of files to keep: {}".format(len(files_to_keep)))

        end_time = time.time()
        print("{0} duplicates has been founded in {1} seconds".format(len(files_to_remove) + len(files_to_keep),
                                                                      end_time - start_time))

        return files_to_keep, files_to_remove, dict_image_to_duplicates

    def show_duplicates(self, image_to_duplicates, output_path, image_w, image_h):
        """
        Show duplicates.
        :return:
        """
        print('Showing duplicates...')
        for image, duplicates in tqdm(image_to_duplicates.items()):
            files_to_show = []

            image_path = self.df_dataset.iloc[image]['file']
            files_to_show.append(ImgUtils.scale(ImgUtils.read_image_numpy(image_path, image_w, image_h)))

            duplicates_path = [f for f in list(self.df_dataset.iloc[duplicates]['file'])]
            duplicates_arr = [ImgUtils.scale(ImgUtils.read_image_numpy(f, image_w, image_h)) for f in duplicates_path]
            files_to_show.extend(duplicates_arr)
            fig_acc = plt.figure(figsize=(10, len(files_to_show) * 5))
            plt.imshow(ImgUtils.mosaic_images(np.asarray(files_to_show), len(files_to_show)))
            fig_acc.savefig(os.path.join(output_path, image_path.split(os.path.sep)[-1]))
            # plt.show()
            plt.cla()
            plt.close()
