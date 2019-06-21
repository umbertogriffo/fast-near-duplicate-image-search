import os

import pytest

from commands.delete import delete
from tests.conftest import mkdir_output, PROJECT_DIR


@pytest.mark.parametrize(
    'hash_size, distance_metric, nearest_neighbors, leaf_size, parallel, batch_size, threshold, '
    'backup_keep, backup_duplicate, safe_deletion, expected',
    [(8, 'manhattan', 5, 40, False, 32, 40, True, True, True,
      [12, '2018-12-11-15-031193.png', '2018-12-11-15-031197.png', 414])
     ])
def test_delete(build_potato_dataset, tree_type, hash_size, distance_metric, nearest_neighbors, leaf_size,
                parallel, batch_size, threshold, backup_keep, backup_duplicate, safe_deletion, expected):
    output_path = mkdir_output(os.path.join(str(PROJECT_DIR), "outputs"))
    df_dataset, img_file_list = build_potato_dataset

    to_keep, to_remove = delete(df_dataset, img_file_list, output_path, hash_size, tree_type, distance_metric,
                                nearest_neighbors, leaf_size, parallel, batch_size, threshold, backup_keep,
                                backup_duplicate, safe_deletion)
    assert len(to_keep) == expected[0]
    assert to_keep[0].split(os.sep)[-1] == expected[1]
    assert to_keep[1].split(os.sep)[-1] == expected[2]
    assert len(to_remove) == expected[3]

    # delete_output(output_path)

    print()


@pytest.mark.parametrize(
    'hash_size, distance_metric, nearest_neighbors, leaf_size, parallel, batch_size, threshold, '
    'backup_keep, backup_duplicate, safe_deletion, expected',
    [(8, 'manhattan', 2, 40, False, 32, 40, True, True, True,
      [15, '2018-12-11-15-031193.png', '2018-12-11-15-031196.png', 15]),
     (8, 'manhattan', 5, 40, False, 32, 40, True, True, True,
      [4, '2018-12-11-15-031193.png', '2018-12-11-16-121735.png', 28]),
     (8, 'manhattan', 10, 40, False, 32, 40, True, True, True,
      [4, '2018-12-11-15-031193.png', '2018-12-11-16-121735.png', 28])
     ])
def test_delete_multi_folder(build_potato_multi_folder_dataset, tree_type, hash_size, distance_metric,
                             nearest_neighbors, leaf_size, parallel, batch_size, threshold, backup_keep,
                             backup_duplicate, safe_deletion, expected):
    output_path = mkdir_output(os.path.join(str(PROJECT_DIR), "outputs"))
    df_dataset, img_file_list = build_potato_multi_folder_dataset

    to_keep, to_remove = delete(df_dataset, img_file_list, output_path, hash_size, tree_type, distance_metric,
                                nearest_neighbors, leaf_size, parallel, batch_size, threshold, backup_keep,
                                backup_duplicate, safe_deletion)
    assert len(to_keep) == expected[0]
    assert to_keep[0].split(os.sep)[-1] == expected[1]
    assert to_keep[3].split(os.sep)[-1] == expected[2]
    assert len(to_remove) == expected[3]

    # delete_output(output_path)

    print()
