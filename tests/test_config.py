import unittest
import tempfile
import shutil
import sys
import os


from pathlib import Path
from pprint import pprint
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config_manager import ConfigManager
from exceptions import *


class TestConfigManager(unittest.TestCase):
    def setUp(self):
        """Создаем временную папку для тестов"""
        self.test_dir = Path(tempfile.mkdtemp(prefix="config_test_"))
        self._create_test_file()

    def tearDown(self):
        """Удаляем временную папку"""
        try:
            if self.test_dir.exists() and self.test_dir.is_dir():
                shutil.rmtree(self.test_dir, ignore_errors=True)
        except Exception as e:
            print(f"Ошибка при удалении папки: {e}")

    def _create_test_file(self):
        # self.test_dir = tempfile.mkdtemp(prefix='test_config_', suffix='_tmp')

        files = ["one.conf", "two.conf", "lol.lol", "rofl.lol"]

        for file in files:
            path = Path(self.test_dir) / file
            path.write_text("config text", encoding="utf-8")

    def test_init_default_config_manager(self):
        """Тест: папка по умолчанию создается"""
        # Переопределяем временно DEFAULT папку через патч
        # import config_manager
        original_default = ConfigManager._DEFAULT_CONFIG_FOLDER

        try:
            # Подменяем на временную папку
            test_default = self.test_dir / "default_conf"
            ConfigManager._DEFAULT_CONFIG_FOLDER = test_default

            config = ConfigManager()

            self.assertTrue(test_default.exists())
            self.assertEqual(config.config_folder, test_default)
        finally:
            # Возвращаем как было
            ConfigManager._DEFAULT_CONFIG_FOLDER = original_default

    # @patch('config_manager.ConfigManager._DEFAULT_CONFIG_FOLDER')
    # def test_init_default_config_manager_var_2(self, mock_default):

    #     fake_default = self.test_dir / "default_conf"

    #     mock_default.return_value = fake_default
    #     config = ConfigManager()
    #     self.assertEqual(config.config_folder, fake_default)
    #     self.assertTrue((self.test_dir / "default_conf").exists())

    def test_set_folder(self):
        """Тест: установка конкретной папки"""
        custom_folder = self.test_dir / "custom_folder"
        config = ConfigManager(custom_folder)

        self.assertTrue(custom_folder.exists())
        self.assertEqual(config.config_folder, custom_folder)

    def test_get_list_config_file(self):
        """Тест: получение списка файлов по расширениям"""
        config = ConfigManager(self.test_dir)
        result = config.get_list_config_file()

        expected_extentions = ["*.conf"]
        expected = []
        expected.extend(
            file
            for ext in expected_extentions
            for file in Path(self.test_dir).glob(ext)
        )
        self.assertEqual(result, expected)

    def test_add_config_file_invalid_exception(self):
        """Тест: добавление файла с неверным расширением вызывает ValueError"""
        # Создаём файл с недопустимым расширением
        bad_file = Path(self.test_dir) / "bad_config.bad"
        bad_file.write_text("very bad file", encoding="utf-8")

        config = ConfigManager(self.test_dir)

        # Проверяем, что выбрасывается FileExtensionError
        with self.assertRaises(FileExtensionError) as context:
            config.add_config_file(bad_file)

        # Дополнительно проверяем сообщение исключения
        self.assertIn("Неверное расширение файла", str(context.exception))
        self.assertIn(".bad", str(context.exception))

    def test_add_config_file_valid(self):
        """Добавление файла с правильным расширением и его копирование"""
        # sub_dir = Path(self.test_dir) / 'sub_dir'
        self.test_dir2 = Path(tempfile.mkdtemp(prefix="config_test_2"))
        valid_file = Path(self.test_dir2) / "valid.conf"

        valid_file.write_text("valide config file", encoding="utf-8")

        config = ConfigManager(self.test_dir)
        config.add_config_file(valid_file)

        # Проверяем, что файл скопирован в папку конфигураций
        copied_file = self.test_dir / "valid.conf"
        self.assertTrue(copied_file.exists())


if __name__ == "__main__":
    unittest.main()
