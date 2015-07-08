import configparser
import os
import shutil
import hashlib

class PackagerException(Exception):
    pass


class PackagerConfig(object):
    """Config reader for pyconfigs declaration
    """
    def __init__(self, config_file):
        self.pyconfigs = configparser.ConfigParser()
        self.pyconfigs.read(config_file)

        self.root = self.pyconfigs['DEFAULT']['root']
        self.__maybe_construct_folders()
    
    def __maybe_construct_folders(self):
        if not os.path.exists(self.root) or not os.path.isdir(self.root):
            os.makedirs(self.get_test_folder())
            os.makedirs(self.get_code_folder())

    def get_test_folder(self):
        return os.path.join(self.root, self.pyconfigs['DEFAULT']['test'])

    def get_code_folder(self):
        return os.path.join(self.root, self.pyconfigs['DEFAULT']['code'])

    def purge_directories(self):
        if self.pyconfigs['DEFAULT']['allow_purge']:
           shutil.rmtree(self.root) 
        else:
            raise PackagerException("not allowed to purge directories")


class Packager(object):
    """The base packager factory for creating and retrieving packaged code/test pairs.
    Contains a staticmethod to create unit key based on question name.
    """
    def __init__(self, packager_config):
        self.set_configs(packager_config) 

    def set_configs(self, packager_config):
        self.packager_config = packager_config

    @staticmethod
    def generate_key(name):
        """Uses simple hashlib methods to create a unique ID for this question.
        """
        return hashlib.md5(name.encode('utf-8')).hexdigest()


class PythonPackager(Packager):
    """
    """

    def bundle(self, question_name, code_str, test_str):
       key = Packager.generate_key(question_name) 


class JavaPackager(Packager):
    """TODO: build out java land
    """
    pass
