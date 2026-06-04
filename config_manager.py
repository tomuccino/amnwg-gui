import os
import shutil
from pathlib import Path
from typing import Optional

from pprint import pprint

class ConfigManager:
    """ Управление конфигурацией приложения """

    # Папка по умолчанию для хранения конфигов
    # DEFAULT_CONFIG_DIR = Path.home() / ".vpn_configs"
    _DEFAULT_CONFIG_FOLDER: Path = Path("./conf")
    _config_folder: Optional[Path] = None

    def __init__(self, path_to_folder: Optional[Path] = None):
        # Устанавливаем путь: либо переданный, либо по умолчанию
        self._config_folder = (
            path_to_folder if path_to_folder is not None
            else self._DEFAULT_CONFIG_FOLDER
        )
        self._create_config_folder()

    def _create_config_folder(self) -> None:
        """
        Создать папку для конфигов, если её нет
        
        Args:
            pass
            
        Returns:
            bool: Успешность операции
        """
        try:
            folder = Path(self._config_folder)
            folder.mkdir(parents=True, exist_ok=True)

            # Переносим существующие конфиги в новую папку (опционально)
            # ...

        except OSError as e:
            raise OSError(f"Ошибка создания папки {self._config_folder}: {e}") from e


    @property
    def config_folder(self) -> Path:
        """Получаем папку для конфигов"""
        return self._config_folder
    
    @config_folder.setter
    def config_folder(self, new_path: Path) -> None:
        self._config_folder = Path(new_path)
        

if __name__ == '__main__':

    config = ConfigManager('./lol')
    # config._create_default_folder()
    # config.config_folder = './lol'
    # config._create_new_config_folder()
    print(vars(config))
