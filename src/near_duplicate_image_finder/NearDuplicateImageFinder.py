import multiprocessing
import os
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from utils.ImgUtils import ImgUtils

"""
(C) Umberto Griffo, 2019
"""


class NearDuplicateImageFinder(object):

    def __init__(self, df_dataset, leaf_size=40, parallel=False, batch_size=32, verbose=0):

        self.leaf_size = leaf_size
        self.parallel = parallel
        self.batch_size = batch_size
        self.verbose = verbose

        self.df_dataset = df_dataset
        self.tree = None

        if self.parallel:
            number_of_cpu = multiprocessing.cpu_count()
            print("CPU: {}".format(number_of_cpu))

            if number_of_cpu >= 2:
                self.number_of_cpu = number_of_cpu
            else:
                raise ValueError("Number of CPU must greater than or equal to 2.")

        self.build_tree()

    @staticmethod
    def __getThreads():
        """ Returns the number of available threads on a posix/win based system """
        if sys.platform == 'win32':
            return (int)(os.environ['NUMBER_OF_PROCESSORS'])
        else:
            return (int)(os.popen('grep -c cores /proc/cpuinfo').read())

    def build_tree(self):
        raise NotImplementedError('subclasses must override build_tree()!')

    def _find(self, image_id, nearest_neighbors=5, threshold=10):
        raise NotImplementedError('subclasses must override find()!')

    def _find_all(self, nearest_neighbors=5, threshold=10):
        raise NotImplementedError('subclasses must override find_all()!')

    def find_near_duplicates(self, image_id, nearest_neighbors=5, threshold=10):
        """
        Find near duplicates of an image.
        :param image_id:
        :param nearest_neighbors:
        :param threshold:
        :return:
        """
        print('Finding duplicates...')
        start_time = time.time()

        distances, indices = self._find(image_id, nearest_neighbors, threshold)
        max_distance = distances.max()
        print("\t Max distance: {}".format(max_distance))
        # Find the indices of distances elements that are non-zero and less or equal to threshold_in.
        above_threshold_idx = np.argwhere((distances <= threshold) & (distances > 0))
        positions = [i[1] for i in above_threshold_idx]

        above_threshold_distances = []
        above_threshold_indices = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx != image_id and i in positions:
                above_threshold_distances.append(distance)
                above_threshold_indices.append(idx)

        end_time = time.time()

        print("{0} duplicates has been founded in {1} seconds".format(len(above_threshold_indices),
                                                                      end_time - start_time))
        return above_threshold_distances, above_threshold_indices

    def find_all_near_duplicates(self, nearest_neighbors=5, threshold=10):
        """
        Find near duplicated images.
        :param nearest_neighbors:
        :param threshold:
        :return: files_to_keep, files_to_remove, dict_image_to_duplicates
        """

        print('Finding duplicates...')
        start_time = time.time()

        dict_image_to_duplicates = dict()
        keep = []
        remove = []
        # 'distances' is a matrix NxM where N is the number of images and M is the value of nearest_neighbors_in.
        # For each image it contains an array containing the distances of k-nearest neighbors.
        # 'indices' is a matrix NxM where N is the number of images and M is the value of nearest_neighbors_in.
        # For each image it contains an array containing the indices of k-nearest neighbors.
        distances, indices = self._find_all(nearest_neighbors, threshold)
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
        for k, (key, value) in tqdm(enumerate(dict_image_to_duplicates.items())):
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
        print("{0} duplicates has been founded in {1} seconds".format(len(files_to_remove),
                                                                      end_time - start_time))

        return files_to_keep, files_to_remove, dict_image_to_duplicates

    def show_an_image_duplicates(self, image_to_duplicates, image, output_path, image_w, image_h):
        """
        Show near duplicates.
        :param image_to_duplicates:
        :param image:
        :param output_path:
        :param image_w:
        :param image_h:
        :return:
        """

        print('Showing duplicates...')
        duplicate = image_to_duplicates[image]
        files_to_show = []

        image_path = self.df_dataset.iloc[image]['file']
        files_to_show.append(ImgUtils.scale(ImgUtils.read_image_numpy(image_path, image_w, image_h)))

        duplicates_path = [f for f in list(self.df_dataset.iloc[duplicate]['file'])]
        for path in duplicates_path:
            print(path)
        duplicates_arr = [ImgUtils.scale(ImgUtils.read_image_numpy(f, image_w, image_h)) for f in duplicates_path]
        files_to_show.extend(duplicates_arr)
        fig_acc = plt.figure(figsize=(10, len(files_to_show) * 5))
        plt.imshow(ImgUtils.mosaic_images(np.asarray(files_to_show), len(files_to_show)))
        fig_acc.savefig(os.path.join(output_path, image_path.split(os.path.sep)[-1]))
        if self.verbose == 1:
            plt.show()
        plt.cla()
        plt.close()
