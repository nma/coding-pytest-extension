from test.base_test_case import BaseTestCase
import os


class TestParseConfigs(BaseTestCase):

    def test_root_folder_exists(self):
        self.assertTrue(os.path.exists(self.packager_config.root))
        self.assertTrue(os.path.isdir(self.packager_config.root))

    def test_sub_folder_exists(self):
        self.assertTrue(os.path.exists(self.packager_config.get_test_folder()))
        self.assertTrue(os.path.exists(self.packager_config.get_code_folder()))
        self.assertTrue(os.path.isdir(self.packager_config.get_test_folder()))
        self.assertTrue(os.path.isdir(self.packager_config.get_code_folder()))
