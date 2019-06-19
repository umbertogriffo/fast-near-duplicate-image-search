
.PHONY: clean setup test

SHELL=/bin/bash
CONDACTIVATE:= $(shell which activate)

all: setup test package

clean:
	rm -rf .cache/
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/
	rm -rf outputs/
	rm -rf src/deduplication.egg-info

check:
	which conda
	which activate
	which pip
	which python

setup:
	echo $(CONDACTIVATE)
	source $(CONDACTIVATE) && conda env create -f environment.yml && conda deactivate

test:
	echo $(CONDACTIVATE)
	source $(CONDACTIVATE) fast_near_duplicate_img_src_py3 && pytest -s -vv;

package:
	python setup.py sdist bdist_wheel;
