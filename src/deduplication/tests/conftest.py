import datetime
import os

import pytest

from dataset.ImageToHash import ImageToHash
from utils.FileSystem import FileSystem

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = FileSystem.find_a_specific_parent_dir(ROOT_DIR, "fast-near-duplicate-image-search")
CALTECH_101_BASE_PATH = os.path.join(str(PROJECT_DIR), "datasets", "caltech_101_rand_resize")
POTATOES_BASE_PATH = os.path.join(str(PROJECT_DIR), "datasets", "potatoes")
POTATOES_MULTI_FOLDER_BASE_PATH = os.path.join(str(PROJECT_DIR), "datasets", "potatoes_multi_folder")


def mkdir_output(output_path_in):
    dt = str(datetime.datetime.today().strftime('%Y-%m-%d-%H-%M%--S-%f'))

    output_path = os.path.join(output_path_in, dt)
    FileSystem.mkdir_if_not_exist(output_path)

    return output_path


def delete_output(output_path_in):
    FileSystem.remove_dir_if_exist(output_path_in)


def checkEqual(L1, L2):
    return len(L1) == len(L2) and sorted(L1) == sorted(L2)


@pytest.fixture(scope="package", params=[False, True])
def build_potato_dataset(request):
    df_dataset, img_file_list = ImageToHash(POTATOES_BASE_PATH,
                                            hash_size=8,
                                            hash_algo='phash').build_dataset(
        parallel=request.param,
        batch_size=32)

    return df_dataset, img_file_list


@pytest.fixture(scope="package", params=[False, True])
def build_potato_multi_folder_dataset(request):
    df_dataset, img_file_list = ImageToHash(POTATOES_MULTI_FOLDER_BASE_PATH,
                                            hash_size=8,
                                            hash_algo='phash').build_dataset(
        parallel=request.param,
        batch_size=32)

    return df_dataset, img_file_list


@pytest.fixture(scope="package", params=[8])
def hash_size(request):
    return request.param


@pytest.fixture(scope="package", params=['KDTree', 'cKDTree'])
def tree_type(request):
    return request.param


@pytest.fixture(scope="package", params=['manhattan'])
def distance_metric(request):
    return request.param
