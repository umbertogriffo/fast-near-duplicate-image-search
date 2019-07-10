Installation On Ubuntu 18.04
============================

### Option 1: TL;DR
The best way to install (and uninstall) this app is to use pip (pip3 for Python 3). 
In the root directory of the CLI source code, running `install.sh` will install this app using setup.py as “instructions”. 
Likewise, running `uninstall.sh` will remove the app.

### Option 2: Anaconda 
#### Install Anaconda 3-2019.03-Linux-x86_64 

https://repo.anaconda.com/archive/
```
cd /tmp
curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
sha256sum Anaconda3-2019.03-Linux-x86_64.sh
```
 45c851b7497cc14d5ca060064394569f724b67d9b5f98a926ed49b834a6bb73a
```
bash Anaconda3-2019.03-Linux-x86_64.sh
```
#### To verify the installation
```
conda info
conda list
```
#### Create the environment using `fast_near_duplicate_img_src_py3.yml`:
```
conda env create -f fast_near_duplicate_img_src_py3.yml
```

### Option 3: Step-by-step installation
Install Anaconda as showed at previous point.
Make sure that your conda is setup properly with the right environment
for that, check that `which conda`, `which pip` and `which python` points to the
right path. From a clean conda env, this is what you need to do.
##### Let’s create an Anaconda environments
```
conda create -n fast_near_duplicate_img_src_py3 python=3.6
```

 To activate this environment, use:
 > conda activate fast_near_duplicate_img_src_py3

 To deactivate an active environment, use:
 > conda deactivate

##### Install dependencies
```
source activate fast_near_duplicate_img_src_py3
conda install pip pandas scikit-learn scipy numpy matplotlib seaborn pillow natsort==5.5.0 tqdm

# ImageHash 4.0 - Image Hashing library
pip install ImageHash

# OpenCV 4.0.0.21 (Not Mandatory)
apt install libgtk2.0-dev python3-tk
pip install opencv-contrib-python==4.0.0.21

# Pytest 4.1.1 in order to develop Unit/Mock test
pip install -U pytest

# Versioneer 0.18 in order to manage the version number (used by pandas and matplotlib)
# https://github.com/warner/python-versioneer
pip install versioneer

```
See [INSTALL.md](https://github.com/warner/python-versioneer/blob/master/INSTALL.md) in order to use versioneer.
