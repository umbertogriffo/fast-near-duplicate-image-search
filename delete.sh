#!/usr/bin/env bash
source activate fast_near_duplicate_img_src_py3
python3 src/deduplication/__main__.py delete \
--images-path datasets/potatoes \
--output-path outputs \
--tree-type KDTree \
--threshold 40 \
--parallel f \
--nearest-neighbors 5 \
--hash-algorithm phash \
--hash-size 8 \
--distance-metric manhattan \
--backup-keep y \
--backup-duplicate y \
--safe-deletion y
