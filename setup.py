#!/usr/bin/env python
# coding: utf-8
# Package and distribution management.

from setuptools import setup, find_packages

with open('LICENSE') as f:
    license = f.read()

setup(
    name='deduplication',
    version='0.1.0',
    description='Fast Near-Duplicate Image Search and Delete.',
    long_description='This Python script is a command line tool for visualizing, checking and deleting near-duplicate '
                     'images from the target directory.',
    author='Umberto Griffo',
    author_email='umberto.griffo@gmail.com',
    url='https://github.com/umbertogriffo/fast-near-duplicate-image-search',
    license=license,
    packages=find_packages(exclude=("tests","experiments",)),
    include_package_data=True,
    install_requires=[
        "certifi==2019.3.9"
        , "cycler==0.10.0"
        , "ImageHash==4.0"
        , "kiwisolver==1.0.1"
        , "matplotlib==3.0.3"
        , "mkl-fft==1.0.6"
        , "mkl-random==1.0.1.1"
        , "natsort==5.5.0"
        , "numpy==1.16.2"
        , "olefile==0.44"
        , "opencv-contrib-python==4.0.0.21"
        , "pandas==0.24.2"
        , "patsy==0.5.1"
        , "Pillow==6.0.0"
        , "pyparsing==2.4.0"
        , "python-dateutil==2.8.0"
        , "pytz==2019.1"
        , "PyWavelets==1.0.3"
        , "scikit-learn==0.20.3"
        , "scipy==1.2.1"
        , "seaborn==0.9.0"
        , "six==1.12.0"
        , "statsmodels==0.9.0"
        , "tornado==6.0.2"
        , "tqdm==4.31.1"],
    entry_points={
        'console_scripts': [
            'deduplication = deduplication.__main__:main'
        ]
    }
)
