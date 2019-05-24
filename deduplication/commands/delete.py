import random

from deduplication.commands.helpers import get_images_list, build_tree, save_results
from deduplication.dataset.ImageToHashDataset import ImageToHashDataset


def delete(images_path,
           output_path,
           hash_algo,
           hash_size,
           tree_type,
           distance_metric,
           nearest_neighbors,
           leaf_size,
           parallel,
           batch_size,
           threshold,
           delete_keep,
           image_w,
           image_h):
    # Retrieve the images contained in output_path.
    img_file_list = get_images_list(images_path, natural_order=True)
    # Build the dataset
    df_dataset = ImageToHashDataset(img_file_list, hash_size=hash_size, hash_algo=hash_algo).build_dataset(
        parallel=parallel,
        batch_size=batch_size)
    # Build the tree
    near_duplicate_image_finder = build_tree(df_dataset, tree_type, distance_metric, leaf_size, parallel,
                                             batch_size)
    # Find duplicates
    to_keep, to_remove, dict_image_to_duplicates = near_duplicate_image_finder.find_all_near_duplicates(
        nearest_neighbors,
        threshold)
    total_report = to_keep + to_remove
    print('We have found {0}/{1} duplicates in folder'.format(len(to_remove), len(img_file_list)))
    # Save results
    save_results(img_file_list, to_keep, to_remove, hash_size, threshold, output_path, delete_keep_in=delete_keep)
    # Show a duplicate
    if len(dict_image_to_duplicates) > 0:
        random_img = random.choice(list(dict_image_to_duplicates.keys()))
        near_duplicate_image_finder.show_an_image_duplicates(dict_image_to_duplicates, random_img, output_path,
                                                             image_w=image_w,
                                                             image_h=image_h)
