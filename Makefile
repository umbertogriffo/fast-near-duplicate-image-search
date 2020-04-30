.PHONY: check clean setup-env export-env test lint package

all: check clean setup-env test package

clean:
	rm -rf .pyenv/
	rm -rf .cache/
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/
	rm -rf outputs/
	rm -rf src/deduplication.egg-info

check:
	which pip3
	which python3

setup-env:
	virtualenv .pyenv; \
    . .pyenv/bin/activate; \
    pip3 install -r requirements.txt; \

export-env:
	. .pyenv/bin/activate; \
    pip3 freeze > requirements.txt

test:
	. .pyenv/bin/activate; \
	pytest -s -vv;
	rm -rf outputs/

lint:
	. .pyenv/bin/activate; \
    python3 -m pylint src/deduplication; \

package:
	python setup.py sdist bdist_wheel;
