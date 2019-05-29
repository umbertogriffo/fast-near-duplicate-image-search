import os

import pytest

from commands.delete import delete
from tests.conftest import delete_output, mkdir_output, PROJECT_DIR


@pytest.mark.parametrize(
    'hash_size, tree_type, distance_metric, nearest_neighbors, leaf_size, parallel, batch_size, threshold, '
    'delete_keep, image_w, image_h, expected',
    [(8, 'KDTree', 'manhattan', 10, 40, False, 32, 40, False, 128, 128,
      [74, '2018-12-11-15-031193.png', '2018-12-11-15-031197.png', 349]),
     (8, 'cKDTree', 'manhattan', 10, 40, False, 32, 40, False, 128, 128,
      [76, '2018-12-11-15-031193.png', '2018-12-11-15-031197.png', 347])
     ])
def test_delete(build_potato_dataset, hash_size, tree_type, distance_metric, nearest_neighbors, leaf_size,
                parallel, batch_size, threshold, delete_keep, image_w, image_h, expected):
    output_path = mkdir_output(os.path.join(str(PROJECT_DIR), "outputs"))
    df_dataset, img_file_list = build_potato_dataset

    to_keep, to_remove = delete(df_dataset,
                                img_file_list,
                                output_path,
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
                                image_h)
    assert len(to_keep) == expected[0]
    assert to_keep[0].split(os.sep)[-1] == expected[1]
    assert to_keep[1].split(os.sep)[-1] == expected[2]
    assert len(to_remove) == expected[3]

    delete_output(output_path)

    print()
