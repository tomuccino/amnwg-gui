from pathlib import Path
from config_manager import ConfigManager


class VPNController:
    """Контроллер между GUI и ConfigManager

    Атрибуты:
        _config_manager (ConfigManager): менеджер управления конфигурациями.
        _config_folder (Path): папка с конфигурациями.
    """

    _config_manager: ConfigManager
    # _config_folder: Path

    def __init__(self, config_manager: ConfigManager):
        """Устанавливаем config_manager

        Args:
                config_manager (ConfigManager): менеджер управления конфигурациями
        """
        if not isinstance(config_manager, ConfigManager):
            raise TypeError(
                f"config_manager должен быть экземпляром ConfigManager, "
                f"получено: {type(config_manager).__name__}"
            )
        self._config_manager = config_manager
        # self._config_folder = config_manager.config_folder

    @property
    def config_folder(self) -> Path:
        """Получаеи текущую папку с конфигами"""
        return self._config_manager.config_folder

    def change_config_folder(self, new_folder: Path) -> Path:
        """Меняем папку с конфигами на новую

        Args:
            new_folder (Path): новая папка для конфигов
        """
        self._config_manager.config_folder = new_folder
        return self._config_manager.config_folder

    def reset_config_folder(self) -> Path:
        """Сбрасываем текущую папку с конфигами на дефолтную"""
        return self._config_manager.default_config_folder

    def get_list_config_file(self) -> list[Path]:
        """Получаем список конфигов в папке"""
        return self._config_manager.get_list_config_file()
