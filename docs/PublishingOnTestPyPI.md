#### Generating distribution archives
Make sure you have the latest versions of `setuptools` and `wheel` installed:
```
python3 -m pip install --user --upgrade setuptools wheel
```

Create a source distribution with:
```
$ python setup.py sdist bdist_wheel
```
This will create `dist/deduplication-0.1.0.tar.gz` inside our top-level directory. 
The `tar.gz` file is a **source archive** whereas the `.whl` file is a **built distribution**.
If you like, copy that file to another host and try unpacking it and install it, just to verify that it works for you.

#### Uploading the distribution archives
The first thing you’ll need to do is register an account on `Test PyPI`.
`Test PyPI` is a separate instance of the package index intended for testing and experimentation. 
It’s great for things like this tutorial where we don’t necessarily want to upload to the real index. 
To register an account, go to https://test.pypi.org/account/register/ and complete the steps on that page.
You will also need to verify your email address before you’re able to upload any packages.

Now, you can use `twine` to upload the distribution packages. You’ll need to install Twine:
```
python3 -m pip install --user --upgrade twine
```
Once installed, run `Twine` to upload all of the archives under dist:
```
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```
You will be prompted for the username and password you registered with `Test PyPI`. 
After the command completes, you should see output similar to this:
```
Uploading distributions to https://test.pypi.org/legacy/
Enter your username: [your username]
Enter your password:
Uploading example_pkg_your_username-0.0.1-py3-none-any.whl
100%|█████████████████████| 4.65k/4.65k [00:01<00:00, 2.88kB/s]
Uploading example_pkg_your_username-0.0.1.tar.gz
100%|█████████████████████| 4.25k/4.25k [00:01<00:00, 3.05kB/s]
```
Once uploaded your package should be viewable on `TestPyPI` https://test.pypi.org/project/deduplication/

More info on: https://packaging.python.org/tutorials/packaging-projects/