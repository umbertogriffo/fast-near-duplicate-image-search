import os
import shutil
from pathlib import Path


class FileSystem(object):

    @staticmethod
    def mkdir_if_not_exist(directory):

        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

    @staticmethod
    def remove_dir_if_exist(directory):

        if os.path.exists(directory):
            if os.path.isdir(directory):
                try:
                    shutil.rmtree(directory)
                except OSError as e:
                    print("Error: %s - %s." % (e.filename, e.strerror))

    @staticmethod
    def remove_file(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

    @staticmethod
    def copy_file(file_path, dest_path):
        if os.path.isfile(file_path):
            try:
                shutil.copy(file_path, dest_path)
            except IOError as e:
                print("Unable to copy file. %s" % e)

    @staticmethod
    def find_a_specific_parent_dir(file_path, parent_dir_name):
        if str(file_path) == os.path.sep:
            raise ValueError("{} doesn't exist".format(parent_dir_name))
        if str(Path(file_path).parent).split(os.path.sep)[-1] == parent_dir_name:
            return Path(file_path).parent
        else:
            return FileSystem.find_a_specific_parent_dir(Path(file_path).parent, parent_dir_name)
