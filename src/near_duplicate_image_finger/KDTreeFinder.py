from sklearn.neighbors import KDTree

from near_duplicate_image_finger.NearDuplicateImageFinder import NearDuplicateImageFinder


class KDTreeFinder(NearDuplicateImageFinder):

    def __init__(self, img_file_list, hash_size=16, leaf_size=40, parallel=False, batch_size=32, verbose=0):
        super().__init__(img_file_list, hash_size, leaf_size, parallel, batch_size, verbose)

    def build_tree(self):
        print('Building the KDTree...')

        hash_str_len = len(self.df_dataset.at[0, 'hash_list'])
        self.tree = KDTree(self.df_dataset[[str(i) for i in range(0, hash_str_len)]], leaf_size=self.leaf_size,
                           metric='manhattan')

    def find(self, nearest_neighbors=10, threshold=150):
        hash_str_len = len(self.df_dataset.at[0, 'hash_list'])
        # 'distances' is a matrix NxM where N is the number of images and M is the value of nearest_neighbors_in.
        # For each image it contains an array containing the distances of k-nearest neighbors.
        # 'indices' is a matrix NxM where N is the number of images and M is the value of nearest_neighbors_in.
        # For each image it contains an array containing the indices of k-nearest neighbors.
        distances, indices = self.tree.query(self.df_dataset[[str(i) for i in range(0, hash_str_len)]],
                                             k=nearest_neighbors)

        return distances, indices
