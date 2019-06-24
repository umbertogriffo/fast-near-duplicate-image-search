# Fast Near-Duplicate Image Search and Delete
* Author: Umberto Griffo
* Twitter: @UmbertoGriffo

This Python script is a command line tool for visualizing, checking and deleting near-duplicate images from the target directory.
In order to find similar images this script hashes the images using **pHash** from 
[ImageHash](https://pypi.org/project/ImageHash/) library,
adding the hash into a **KDTree** and perform a **nearest neighbours** search.
In addition, near-duplicate images can be visualized generating a 
[t-SNE (t-distributed Stochastic Neighbor Embedding)](https://lvdmaaten.github.io/tsne/) 
using a feature vector for each image derived from the **pHash** function.
> I take no responsibility for bugs in this script or accidentally deleted pictures. 
> Use at your own risk. Make sure you back up your pictures before using.
> This algorithm is intended to find nearly duplicate images. It is NOT intended to find images that are conceptually 
similar.
## Search
![phases](https://github.com/umbertogriffo/fast-near-duplicate-image-search/blob/master/docs/images/phase.png)
## Deletion
![delete](https://github.com/umbertogriffo/fast-near-duplicate-image-search/blob/master/docs/images/delete.png)

## pHash definition

Features in the image are used to generate a distinct (but not unique) fingerprint, and these fingerprints are comparable.
[Perceptual hashes](http://hackerfactor.com/blog/index.php%3F/archives/432-Looks-Like-It.html) are a different concept 
compared to cryptographic hash functions like **MD5** and **SHA1**.

![phash](https://github.com/umbertogriffo/fast-near-duplicate-image-search/blob/master/docs/images/phash.png)

With cryptographic hashes, the hash values are random. The data used to generate the hash acts like a random seed, 
so the same data will generate the same result, but different data will create different results.
Comparing two **SHA1** hash values really only tells you two things. 
If the hashes are different, then the data is different. 
And if the hashes are the same, then the data is likely the same. 
(Since there is a possibility of a hash collision, having the same hash values does not guarantee the same data.) 
In contrast, perceptual hashes can be compared giving you a sense of similarity between the two data sets.
Using **pHash** images can be scaled larger or smaller, have different aspect ratios, and even minor coloring differences 
(contrast, brightness, etc.) and they will still match similar images.

## KDTree definition
A [KDTree](https://en.wikipedia.org/wiki/K-d_tree)(short for k-dimensional tree) is a space-partitioning data structure for organizing 
points in a k-dimensional space. 
In particular, **KDTree** helps organize and partition the data points based on specific conditions.
KDTree is a useful for several applications, such as searches involving a multidimensional search key (e.g. range searches and nearest neighbor searches).

### Complexity (Average)

|Scape|Search|Insert|Delete|
|-----|-----|-----|-----|
|O(n)|O(log n)|O(log n)|O(log n)|

where **n** is the number of points.

Installation
============
Check [INSTALL.md](docs/INSTALL.md) for installation instructions.

How to use the Makefile
=======================
#### Prerequisites

Install `Anaconda3-5.0.1` see `Option 2` in [INSTALL.md](docs/INSTALL.md)

* All-in-one: ```make all```
  * Setup, test and package
* Setup: ```make setup```
  * Installs all dependencies
* Test: ```make test```
  * Runs all tests
  * Using [pytest](https://pypi.org/project/pytest/)
* Clean: ```make clean```
  * Removes all cached files
* Check: ```make check```
  * Use It to check that `which active`, `which conda`, `which pip` and `which python` points to the
right path
* Package: ```make package```
  * Creates a bundle of software to be installed

**Note:** Run `Setup` as your init command (or after `Clean`)
  
Usage
=====
#### Delete near-duplicate images from the target directory

```
$ deduplication delete --images_path <target_dir> --output_path <output_dir> --tree_type KDTree
```
```
Building the dataset...
 94%|█████████▎| 399/426 [00:01<00:00, 260.90it/s]0 out to 426
100%|██████████| 426/426 [00:01<00:00, 261.02it/s]
Building the KDTree...
Finding duplicates...
	 Max distance: 279.0
	 Min distance: 0.0
305it [00:00, 208654.82it/s]
	 number of files to remove: 237
	 number of files to keep: 128
365 duplicates has been founded in 0.021222591400146484 seconds
We have found 365/426 duplicates in folder
We have found 189/426 not duplicates in folder
```
#### Find near-duplicated images from an image you specified
```
$ deduplication search \
 --images_path <target_dir> \
 --output_path <output_dir> \
 --query <specify a query image file>
```
For example:
```
$ deduplication search \
--images-path datasets/potatoes \
--output-path outputs \
--tree-type KDTree \
--threshold 40 \
--parallel f \
--nearest-neighbors 5 \
--hash-algorithm phash \
--hash-size 8 \
--distance-metric manhattan \
--query datasets/potatoes/2018-12-11-15-031193.png
```

![phases](https://github.com/umbertogriffo/fast-near-duplicate-image-search/blob/master/docs/images/search.png)

#### Show near-duplicate images from the target directory With t-SNE 
```
$ deduplication show --images_path <target_dir> --output_path <output_dir>
```
![phases](https://github.com/umbertogriffo/fast-near-duplicate-image-search/blob/master/docs/images/resized_cluster.png)

Todo
====
- [X] Using t-SNE in order to visualize a clusters of near-duplicate images: 
    - https://www.kaggle.com/colinmorris/visualizing-embeddings-with-t-sne
    - https://github.com/zegami/image-similarity-clustering
    - https://github.com/ml4a/ml4a-guides/blob/master/notebooks/image-tsne.ipynb
- [ ] Looking for inspiration from:
    - https://github.com/philipbl/duplicate-images
    - https://github.com/knjcode/imgdupes
    - https://github.com/EdjoLabs/image-match
    - http://www.tudatech.com/visualsearchapi/?apiDoc=V
- [ ] Trying to use Parallel t-SNE implementation with Python and Torch wrappers.
    - https://github.com/DmitryUlyanov/Multicore-TSNE
- [ ] Trying to use Fast Fourier Transform-accelerated Interpolation-based t-SNE (FIt-SNE)
    - https://github.com/KlugerLab/FIt-SNE
- [ ] Trying to use Extensible, parallel implementations of t-SNE 
    - https://github.com/pavlin-policar/openTSNE
- [ ] Trying to use pykdtree instead of KDTree.
    - https://github.com/storpipfugl/pykdtree
- [ ] Trying to use Locality Sensitive Hashing instead of KDTree.
    - https://towardsdatascience.com/locality-sensitive-hashing-for-music-search-f2f1940ace23
    - https://towardsdatascience.com/fast-near-duplicate-image-search-using-locality-sensitive-hashing-d4c16058efcb
- [ ] Trying to use BK-trees instead of KDTree.
    - http://tech.jetsetter.com/2017/03/21/duplicate-image-detection/
- [ ] You could also use k-means to cluster the images and only search within clusters that are similar to the query. 
   

References
==========

* [ImageHash](https://pypi.org/project/ImageHash/)
* [ImageHash - Official Github repository](https://github.com/JohannesBuchner/imagehash)
* [KDTree - Wikipedia](https://en.wikipedia.org/wiki/K-d_tree)
* [Introductory guide to Information Retrieval using kNN and KDTree](https://www.analyticsvidhya.com/blog/2017/11/information-retrieval-using-kdtree/)
* [Perceptual Hash computation](http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.htm)
* [The complete guide to building an image search engine with Python and OpenCV](https://www.pyimagesearch.com/2014/12/01/complete-guide-building-image-search-engine-python-opencv/)
* [Visualizing Embeddings With t-SNE](https://www.kaggle.com/colinmorris/visualizing-embeddings-with-t-sne)
* [t-SNE visualization of CNN codes](https://cs.stanford.edu/people/karpathy/cnnembed/)
* [Benchmarking Nearest Neighbor Searches in Python](https://jakevdp.github.io/blog/2013/04/29/benchmarking-nearest-neighbor-searches-in-python/)
* [Fingerprinting Images for Near-Duplicate Detection](https://realpython.com/fingerprinting-images-for-near-duplicate-detection/)
* [Image dataset - Caltech 101](http://www.vision.caltech.edu/Image_Datasets/Caltech101/)
