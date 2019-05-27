# USAGE
# python compare.py --image-a images/84eba74d-38ae-4bf6-b8bd-79ffa1dad23a.jpg --image-b images/1a4c0d2c-a478-470b-ba5d-2d02b6c0290a.jpg

import argparse
import numpy as np

import imagehash
from PIL import Image
from sklearn.neighbors import DistanceMetric

hash_algo_list = [imagehash.average_hash, imagehash.dhash, imagehash.phash, imagehash.whash]
# https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.DistanceMetric.html
valid_metrics = [
    'euclidean',
    'l2',
    'minkowski',
    'p',
    'manhattan',
    'cityblock',
    'l1',
    'chebyshev',
    'infinity',
]

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--image-a", required=True,
                help="path to the query image")
ap.add_argument("-b", "--image-b", required=True,
                help="path to the query image")
ap.add_argument("-d", "--distance-metric", required=False,
                help="distance metric")
args = vars(ap.parse_args())

image_a = Image.open(args["image_a"])
image_b = Image.open(args["image_b"])

for hash in hash_algo_list:
    print("\nUsing {}:".format(hash.__name__))

    h_a = str(hash(image_a))
    h_b = str(hash(image_b))
    print(h_a)
    print(h_b)

    print("\nCalculate distance:")
    dist = DistanceMetric.get_metric('manhattan')
    # Convert a hex string to an int
    ndarr_int_h_a = np.array([int(i, 16) for i in h_a]).reshape((1, 16)).astype(int)
    ndarr_int_h_b = np.array([int(i, 16) for i in h_b]).reshape((1, 16)).astype(int)
    # Convert a hex string to binary representation
    ndarr_bin_h_a = hash(image_a).hash.reshape((1, 64)).astype(int)
    ndarr_bin_h_b = hash(image_b).hash.reshape((1, 64)).astype(int)

    print(ndarr_int_h_a)
    print(ndarr_int_h_b)
    dist_int = dist.pairwise(ndarr_int_h_a, ndarr_int_h_b)
    print("{}".format(dist_int[0][0]))

    print(ndarr_bin_h_a)
    print(ndarr_bin_h_b)
    dist_bin = dist.pairwise(ndarr_bin_h_a, ndarr_bin_h_b)
    print("{}".format(dist_bin[0][0]))

