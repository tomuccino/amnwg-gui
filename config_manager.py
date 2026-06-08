import os
import shutil

from pathlib import Path
from typing import Optional

from pprint import pprint
from exceptions import *


class ConfigManager:
    """Управление конфигурацией приложения

    Атрибуты:
        _DEFAULT_CONFIG_FOLDER (Path): Путь папки по умолчанию.
        _EXTENTION (List): расширения файлов конфигураци
        _config_folder [Optional](Path): Папказаданная пользователем.
    """

    _DEFAULT_CONFIG_FOLDER: Path = Path("./conf")
    _EXTENTION: list = [".conf"]
    _config_folder: Optional[Path] = None

    def __init__(self, path_to_folder: Optional[Path] = None):
        """Устанавливаем путь до папки с конфигами

        Args:
                path_to_folder Optional[Path]: Путь до папки
        """
        # Устанавливаем путь: либо переданный, либо по умолчанию
        self._config_folder = (
            path_to_folder
            if path_to_folder is not None
            else self._DEFAULT_CONFIG_FOLDER
        )
        self._create_config_folder()

    def _create_config_folder(self) -> None:
        """
        Создать папку для конфигов

        Берем путь из self._config_folder

        Вызывает:
            OSError: Если не удалось создать папку по указанной причине (например, из‑за проблем с правами доступа).
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
        """Задаем папку для конфигов"""
        self._config_folder = Path(new_path)

    def get_list_config_file(self) -> list[Path]:
        """Получить список всех конфиг-файлов в папке"""
        configs = []

        for ext in self._EXTENTION:
            # Если расширение без '*', добавляем префикс для glob
            if not ext.startswith("*"):
                ext = f"*{ext}"
            configs.extend(self._config_folder.glob(ext))

        return configs

    def add_config_file(self, source_path: Path):
        """Добавить файл в папку с конфигурациями"""
        if source_path.suffix not in self._EXTENTION:
            raise FileExtensionError(
                f"Неверное расширение файла: {source_path.suffix}. Допустимые: {self._EXTENTION}"
            )

        try:
            if source_path.exists():
                shutil.copy2(source_path, self._config_folder)
        except OSError as e:
            raise print(f"Ошибка при копировании файла конфигурации {e}") from e


if __name__ == "__main__":

    config = ConfigManager("./lol")
    # config._create_default_folder()
    # config.config_folder = './lol'
    # config._create_new_config_folder()
    print(vars(config))
