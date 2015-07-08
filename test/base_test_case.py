import unittest
from compilation_builder.python_packager import PackagerConfig
import os


class BaseTestCase(unittest.TestCase):
    """Basic compilation of reusable test compononets
    """

    def setUp(self):
        # get the current directory of this test file
        self.test_directory = os.path.dirname(os.path.realpath(__file__))
        self.packager_config = PackagerConfig(self.get_file("packager_config.cfg")) 

    def tearDown(self):
        self.packager_config.purge_directories()

    def get_file(self, filename):
        return self.test_directory + '/' + filename
