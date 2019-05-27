import sys
import os
print(sys.path)
# In order to solve ModuleNotFoundError after packaging using setuptools
#   - https://stackoverflow.com/questions/48952408/modulenotfounderror-after-packaging-using-setuptools-in-python-3-6
#   - https://askubuntu.com/questions/470982/how-to-add-a-python-module-to-syspath
for path in sys.path:
    if 'src' in path:
        print(os.path.join(path, 'deduplication'))
        sys.path.insert(0, os.path.join(path,'deduplication'))
        break;