#!/usr/bin/env bash
source activate fast_near_duplicate_img_src_py3
python src/app.py search \
--images-path datasets/potatoes \
--output-path outputs \
--tree-type KDTree \
--threshold 40 \
--parallel f \
--nearest-neighbors 10 \
--hash-algorithm phash \
--hash-size 8 \
--distance-metric manhattan \
--query datasets/potatoes/2018-12-11-15-031193.png
