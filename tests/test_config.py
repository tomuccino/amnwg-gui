import unittest
import tempfile
import shutil
import sys
import os

from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self._create_test_file()
        default_config = ConfigManager()
        self.default_folder = default_config._DEFAULT_CONFIG_FOLDER

        config = ConfigManager(self.test_folder)
        print(list(Path(self.test_folder).iterdir()))
    
    def tearDown(self):
        shutil.rmtree(self.default_folder)
        shutil.rmtree(self.test_folder)

    
    def _create_test_file(self):
        self.test_folder = tempfile.mkdtemp(prefix='test_config_', suffix='_tmp')

        files = ['one.conf', 'two.conf', 'lol.lol', 'rofl.lol']

        for file in files:
            path = Path(self.test_folder) / file
            path.write_text('config text', encoding='utf-8')


    def test_init_default_config_manager(self):
        config = ConfigManager()
        folder = config._DEFAULT_CONFIG_FOLDER
        self.assertTrue(Path(folder).exists())

    def test_set_folder(self):
        config = ConfigManager('./test_folder')
        folder = config.config_folder
        self.assertTrue(Path(folder).exists())

if __name__ == '__main__':
    unittest.main()