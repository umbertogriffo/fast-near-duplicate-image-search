from scipy.spatial import cKDTree

from duplicatefinder.NearDuplicateImageFinder import NearDuplicateImageFinder


class cKDTreeFinder(NearDuplicateImageFinder):

    def __init__(self, img_file_list, distance_metric, leaf_size=40, parallel=False, batch_size=32, verbose=0):
        super().__init__(img_file_list, leaf_size, parallel, batch_size, verbose)
        self.distance_metric = distance_metric

    def build_tree(self):
        print('Building the cKDTree...')

        hash_str_len = len(self.df_dataset.at[0, 'hash_list'])
        self.tree = cKDTree(self.df_dataset[[str(i) for i in range(0, hash_str_len)]], leafsize=self.leaf_size)

    def _find_all(self, nearest_neighbors=5, threshold=10):
        n_jobs = 1
        hash_str_len = len(self.df_dataset.at[0, 'hash_list'])
        # 'distances' is a matrix NxM where N is the number of images and M is the value of nearest_neighbors_in.
        # For each image it contains an array containing the distances of k-nearest neighbors.
        # 'indices' is a matrix NxM where N is the number of images and M is the value of nearest_neighbors_in.
        # For each image it contains an array containing the indices of k-nearest neighbors.
        if self.parallel:
            print("\tCPU: {}".format(self.number_of_cpu))
            n_jobs = self.number_of_cpu
        # TODO self.distance_metric for cKDTree is p
        """
        p : float, 1<=p<=infinity
                    Which Minkowski p-norm to use. 
                    1 is the sum-of-absolute-values "Manhattan" distance
                    2 is the usual Euclidean distance
                    infinity is the maximum-coordinate-difference distance
        """
        distances, indices = self.tree.query(self.df_dataset[[str(i) for i in range(0, hash_str_len)]],
                                             k=nearest_neighbors, p=1, distance_upper_bound=threshold,
                                             n_jobs=n_jobs)

        return distances, indices

    def _find(self, image_id, nearest_neighbors=5, threshold=10):
        n_jobs = 1
        if self.parallel:
            n_jobs = self.number_of_cpu

        hash_str_len = len(self.df_dataset.at[0, 'hash_list'])

        distances, indices = self.tree.query(
            self.df_dataset[[str(i) for i in range(0, hash_str_len)]].iloc[image_id].values.reshape(1, -1),
            k=nearest_neighbors, p=1, distance_upper_bound=threshold,
            n_jobs=n_jobs)

        return distances, indices
