from pathlib import Path
from config_manager import ConfigManager

class VPNController():
    """Контроллер между GUI и ConfigManager

    Атрибуты:
        _config_manager (ConfigManager): менеджер управления конфигурациями.
        _config_folder (Path): папка с конфигурациями.
    """
    _config_manager: ConfigManager
    _config_folder: Path

    def __init__(self, config_manager: ConfigManager):
        if not isinstance(config_manager, ConfigManager):
            raise TypeError(
                f"config_manager должен быть экземпляром ConfigManager, "
                f"получено: {type(config_manager).__name__}"
            )
        self._config_manager = config_manager
        self._config_folder = config_manager._config_folder

    def get_config_folder(self):
        self._config_folder = self._config_manager.config_folder
    
    