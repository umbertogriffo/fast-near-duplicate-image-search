Installation 
============

### Option 1: TL;DR
The best way to install (and uninstall) this app is to use pip (pip3 for Python 3). 
In the root directory of the CLI source code, running `install.sh` will install this app using setup.py as “instructions”. 
Likewise, running `uninstall.sh` will remove the app.

### Option 2: Virtualenv 

#### Install Python and Virtualenv on MacOs

Install Brew:
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Install python 3.7+ and virtualenv:

```.env
brew install python3
python3 -m pip install virtualenv
```

#### Install Python and Virtualenv on MacOs Ubuntu 18.04 (it has to be tested)

Install python 3.7+ and virtualenv:

```
apt install -y python3.7 python3-pip
python3 -m pip install virtualenv
```

#### Create the environment using `requirements.txt`:
```
virtualenv .pyenv
. .pyenv/bin/activate
pip3 install -r requirements.txt
```

### Option 3: Step-by-step installation
Install Virtualenv as showed at previous point.
Make sure that your environment is setup properly.
Check that `which pip3` and `which python3` points to the
right path. From a clean Virtualenv env, this is what you need to do.
##### Let’s create a Virtualenv environments
```
virtualenv .pyenv
```

 To activate this environment, use:
 > . .pyenv/bin/activate

 To deactivate an active environment, use:
 > deactivate

##### Install dependencies
```
pip3 install pandas scikit-learn scipy==1.2.1 numpy matplotlib seaborn pillow==6.2.2 natsort==5.5.0 tqdm

# ImageHash 4.0 - Image Hashing library
pip3 install ImageHash==4.0

# Pytest 4.5.0 in order to develop Unit/Mock test
pip3 install -U pytest==4.5.0

# Versioneer 0.18 in order to manage the version number (used by pandas and matplotlib)
# https://github.com/warner/python-versioneer
pip3 install versioneer

# pylint 2.5.0 (https://www.pylint.org/) to check conformance and code smells.
pip3 install pylint==2.5.0

# OpenCV 4.0.0.21 (Not Mandatory)
apt install libgtk2.0-dev python3-tk
pip3 install opencv-contrib-python==4.0.0.21

```
See [INSTALL.md](https://github.com/warner/python-versioneer/blob/master/INSTALL.md) in order to use versioneer.
