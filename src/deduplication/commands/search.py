import os

import matplotlib.pyplot as plt
import numpy as np

from deduplication.commands.helpers import build_tree
from deduplication.utils.ImgUtils import ImgUtils


def search(df_dataset, output_path, tree_type, distance_metric, nearest_neighbors, leaf_size, parallel, batch_size,
           threshold, image_w, image_h, query=None, show=True):

    assert query is not None, "Query can't be None"

    # Build the tree
    near_duplicate_image_finder = build_tree(df_dataset, tree_type, distance_metric, leaf_size, parallel,
                                             batch_size)
    # Get the image's id
    df_image = df_dataset[df_dataset['file'] == query]
    if df_image.empty:
        print("The image doesn't have near duplicates.")
        return [], []
    else:
        image_id = df_image.index.values.astype(int)[0]
        # Find the images's near duplicates
        distances, indices = near_duplicate_image_finder.find_near_duplicates(image_id, nearest_neighbors, threshold)
        # Show the near duplicates
        if len(distances) > 0 and len(indices) > 0:

            for distance, idx in zip(distances, indices):
                print("{0} distance:{1}".format(df_dataset.iloc[idx]['file'], distance))

            image_path = df_dataset.iloc[image_id]['file']
            files_to_show = []
            files_to_show.append(ImgUtils.scale(ImgUtils.read_image_numpy(image_path, image_w, image_h)))

            duplicates_path = [f for f in list(df_dataset.iloc[indices]['file'])]
            duplicates_arr = [ImgUtils.scale(ImgUtils.read_image_numpy(f, image_w, image_h)) for f in duplicates_path]
            files_to_show.extend(duplicates_arr)
            fig_acc = plt.figure(figsize=(10, len(files_to_show) * 5))
            plt.imshow(ImgUtils.mosaic_images(np.asarray(files_to_show), len(files_to_show)))
            fig_acc.savefig(os.path.join(output_path, image_path.split(os.path.sep)[-1]))
            if show:
                plt.show()
            plt.cla()
            plt.close()
            return distances, indices
        else:
            print("The image doesn't have near duplicates.")
            return [], []
