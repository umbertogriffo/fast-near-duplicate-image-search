import random

from commands.helpers import build_tree, save_results


def delete(df_dataset, img_file_list, output_path, hash_size, tree_type, distance_metric, nearest_neighbors,
           leaf_size, parallel, batch_size, threshold, backup_keep, backup_duplicate, safe_deletion, image_w=128,
           image_h=128):
    # Build the tree
    near_duplicate_image_finder = build_tree(df_dataset, tree_type, distance_metric, leaf_size, parallel,
                                             batch_size)
    # Find duplicates
    to_keep, to_remove, dict_image_to_duplicates = near_duplicate_image_finder.find_all_near_duplicates(
        nearest_neighbors,
        threshold)
    print('We have found {0}/{1} duplicates in folder'.format(len(to_remove), len(img_file_list)))
    # Show a duplicate
    if len(dict_image_to_duplicates) > 0:
        random_img = random.choice(list(dict_image_to_duplicates.keys()))
        near_duplicate_image_finder.show_an_image_duplicates(dict_image_to_duplicates, random_img, output_path,
                                                             image_w=image_w,
                                                             image_h=image_h)
    # Save results
    save_results(to_keep, to_remove, hash_size, threshold, output_path, backup_keep, backup_duplicate, safe_deletion)

    return to_keep, to_remove
