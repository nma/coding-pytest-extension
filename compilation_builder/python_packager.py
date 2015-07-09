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

    def __write_to_location(self, folder, key, content):
        file_path = os.path.join(folder, key)
        with open(file_path, 'w') as output:
            output.write(content)

    def get_test_folder(self):
        return os.path.join(self.root, self.pyconfigs['DEFAULT']['test'])

    def get_code_folder(self):
        return os.path.join(self.root, self.pyconfigs['DEFAULT']['code'])

    def save_in_test_folder(self, key, content):
        self.__write_to_location(self.get_test_folder(), key, content)

    def save_in_code_folder(self, key, content):
        self.__write_to_location(self.get_code_folder(), key, content)

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

    @staticmethod
    def generate_key_with_versioning(name, version):
        """Appends a versioning value to the class
        """
        versioned_name = name + "_" + str(version)
        return Packager.generate_key(versioned_name) 


class PythonPackager(Packager):
    """The PythonPackager will hash the code and tests into 2 seperate folders with unique names.
    Will create versioning when requested, otherwise will default to version 1.
    """

    def __construct_meta_data(self, question_name, version):
        return """QUESTION = "{}"
VERSION = {}
KEY = "{}"    
""".format(question_name, version, Packager.generate_key_with_versioning(question_name, version))

    def __get_solution_block(self):
        return """
import unittest, subprocess

def solution(input):
    solutionfile = KEY 
    proc = subprocess.Popen('python solutionfile', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    proc.stdin.write(input)
    out, err = p.communicate()
    return out

"""

    def __update_test_contents(self, question_name, version, test_str):
        updated_test_str = self.__construct_meta_data(question_name, version) + \
                self.__get_solution_block() + \
                test_str
        return updated_test_str

    def bundle(self, question_name, code_str, test_str, version=1):
        key = Packager.generate_key_with_versioning(question_name, version) 
        self.packager_config.save_in_code_folder(key, code_str)
        updated_test_str = self.__update_test_contents(question_name, version, test_str)
        self.packager_config.save_in_test_folder(key, updated_test_str) 
        return key


class JavaPackager(Packager):
    """TODO: build out java land
    """

    def bundle(self, question_name, code_str, test_str, version=1):
        pass

if __name__ == "__main__":
    print(Packager.generate_key_with_versioning("foo", 1))
