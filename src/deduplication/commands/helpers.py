import os

import pandas as pd
from tqdm import tqdm

from duplicatefinder.KDTreeFinder import KDTreeFinder
from duplicatefinder.cKDTreeFinder import cKDTreeFinder
from utils.FileSystem import FileSystem


def backup_images(df_results, output_path_in, column):
    """Backup the images into a folder.

    Parameters
    ----------
    df_results
    output_path_in
    column

    Returns
    -------

    """
    print("Backuping images...")
    with tqdm(total=len(df_results)) as pbar:
        for index, row in df_results.iterrows():

            full_file_name = row[column]

            dest_path = os.path.join(output_path_in, column)
            dstdir = os.path.join(dest_path, os.path.dirname(full_file_name)[1:])
            if not os.path.exists(dstdir):
                os.makedirs(dstdir)  # create all directories
            FileSystem.copy_file(full_file_name, dstdir)
            pbar.update(1)


def delete_images(df_results, column):
    """Delete the images.

    Parameters
    ----------
    df_results
    column

    Returns
    -------

    """
    print("Deleting images...")
    with tqdm(total=len(df_results)) as pbar:
        for index, row in df_results.iterrows():
            full_file_name = row[column]
            FileSystem.remove_file(full_file_name)
            pbar.update(1)


def save_results(to_keep_in, to_remove_in, hash_size_in, threshold_in, output_path_in, backup_keep=True,
                 backup_duplicate=True, safe_deletion=False):
    """

    Parameters
    ----------
    copy_delete
    to_keep_in
    to_remove_in
    hash_size_in
    threshold_in
    output_path_in
    backup_keep
    backup_duplicate

    Returns
    -------

    """
    if len(to_keep_in) > 0:
        to_keep_path = os.path.join(output_path_in,
                                    "duplicates_keep_" + str(hash_size_in) + "_dist_" + str(threshold_in) + ".csv")

        duplicates_keep_df = pd.DataFrame(to_keep_in)
        duplicates_keep_df.columns = ['keep']
        duplicates_keep_df['hash_size'] = hash_size_in
        duplicates_keep_df['threshold'] = threshold_in
        duplicates_keep_df.to_csv(to_keep_path, index=False)
        if backup_keep:
            backup_images(duplicates_keep_df, output_path_in, 'keep')

    if len(to_remove_in) > 0:
        to_remove_path = os.path.join(output_path_in,
                                      "duplicates_remove_" + str(hash_size_in) + "_dist_" + str(threshold_in) + ".csv")
        duplicates_remove_df = pd.DataFrame(to_remove_in)
        duplicates_remove_df.columns = ['remove']
        duplicates_remove_df['hash_size'] = hash_size_in
        duplicates_remove_df['threshold'] = threshold_in
        duplicates_remove_df.to_csv(to_remove_path, index=False)
        if backup_duplicate:
            backup_images(duplicates_remove_df, output_path_in, 'remove')
        if not safe_deletion:
            delete_images(duplicates_remove_df, 'remove')


def build_tree(df_dataset, tree_type, distance_metric_in, leaf_size_in, parallel_in, batch_size_in):
    """

    Parameters
    ----------
    df_dataset
    tree_type
    distance_metric_in
    leaf_size_in
    parallel_in
    batch_size_in

    Returns
    -------

    """
    if tree_type == 'cKDTree':
        near_duplicate_image_finder = cKDTreeFinder(df_dataset, distance_metric=distance_metric_in,
                                                    leaf_size=leaf_size_in,
                                                    parallel=parallel_in, batch_size=batch_size_in)
    elif tree_type == 'KDTree':
        near_duplicate_image_finder = KDTreeFinder(df_dataset, distance_metric=distance_metric_in,
                                                   leaf_size=leaf_size_in,
                                                   parallel=parallel_in, batch_size=batch_size_in)

    return near_duplicate_image_finder
