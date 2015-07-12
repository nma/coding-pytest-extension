import configparser
import os
import shutil
import hashlib
import yaml

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
        """May be exteneded to write to a storage service.
        """
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
    def parse_testcases(bundle):
       """parses the yaml of the test file and returns a list of test input output
       """
       with open(bundle.test_file_path, 'r') as testcases:
           return yaml.load(testcases)

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


class Bundle(object):
    """Model defining a bundle of code, with an accompanyment of tests inputs
    """
    def __init__(self, key, code_folder, test_folder):
        self.key = key
        self.test_file_path = os.path.join(test_folder, key) 
        self.code_file_path = os.path.join(code_folder, key)


class PythonPackager(Packager):
    """The PythonPackager will hash the code and tests into 2 seperate folders with unique names.
    Will create versioning when requested, otherwise will default to version 1.
    """
    def __construct_meta_data(self, question_name, version):
        return """#QUESTION = "{}"
#VERSION = {}
#KEY = "{}"    
""".format(question_name, version, Packager.generate_key_with_versioning(question_name, version))

    def __update_file_contents(self, question_name, version, file_str):
        updated_str = self.__construct_meta_data(question_name, version) + file_str 
        return updated_str

    def __get_bundle(self, key):
        """return a bundle object for a given key.
        """
        code_folder = self.packager_config.get_code_folder()
        test_folder = self.packager_config.get_test_folder()
        if not (os.path.exists(os.path.join(code_folder, key)) and os.path.exists(os.path.join(test_folder, key))):
            raise PackagerException("Bundle with key=" + key + " not found.")

        return Bundle(key, code_folder, test_folder)

    def bundle(self, question_name, code_str, test_str, version=1):
        """makes a bundle that contains the correct metadata and saveds the strings into the correct key 
        """
        key = Packager.generate_key_with_versioning(question_name, version) 
        updated_test_str = self.__update_file_contents(question_name, version, test_str)
        self.packager_config.save_in_test_folder(key, updated_test_str) 
        self.packager_config.save_in_code_folder(key, code_str)
        return self.__get_bundle(key) 

    def execute_bundle(self, key):
        """Given a key, locate the bundle in the storage system, and execute it.
        """
        bundle = self.__get_bundle(key)
        test_cases_dict = Packager.parse_testcases(bundle)


class JavaPackager(Packager):
    """TODO: build out java land
    """

    def bundle(self, question_name, code_str, test_str, version=1):
        pass

if __name__ == "__main__":
    print(Packager.generate_key_with_versioning("foo", 1))
