import os

import pytest

from commands.search import search
from tests.conftest import delete_output, mkdir_output, PROJECT_DIR, POTATOES_BASE_PATH, checkEqual


@pytest.mark.parametrize(
    'tree_type, distance_metric, nearest_neighbors, leaf_size, parallel, batch_size, threshold, '
    'image_w, image_h, query, show, expected',
    [('KDTree', 'manhattan', 5, 40, False, 32, 40, 128, 128,
      os.path.join(POTATOES_BASE_PATH, '2018-12-11-15-031193.png'), False,
      [[8.0, 14.0, 18.0, 22.0], [1, 5, 3, 2]]),
     ('cKDTree', 'manhattan', 5, 40, False, 32, 40, 128, 128,
      os.path.join(POTATOES_BASE_PATH, '2018-12-11-15-031193.png'), False,
      [[8.0, 14.0, 18.0, 22.0], [1, 5, 3, 2]])
     ])
def test_search(build_potato_dataset, tree_type, distance_metric, nearest_neighbors, leaf_size,
                parallel, batch_size, threshold, image_w, image_h, query, show, expected):
    output_path = mkdir_output(os.path.join(str(PROJECT_DIR), "outputs"))
    df_dataset, img_file_list = build_potato_dataset

    distances, indices = search(df_dataset,
                                output_path,
                                tree_type,
                                distance_metric,
                                nearest_neighbors,
                                leaf_size,
                                parallel,
                                batch_size,
                                threshold,
                                image_w,
                                image_h,
                                query, show)

    assert checkEqual(distances, expected[0])
    assert checkEqual(indices, expected[1])

    delete_output(output_path)
