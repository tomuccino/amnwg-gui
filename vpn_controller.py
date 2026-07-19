import os
from pathlib import Path
import subprocess
from typing import Any, Dict
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
        base_dir = os.path.dirname(os.path.abspath(__file__))

        config_folder = os.path.join(base_dir, self._config_manager.config_folder)
        return config_folder
        # return self._config_manager.config_folder

    def _run_cmd(self, cmd, check=True):
        """Запускает команду через subprocess.
        Возвращает (returncode, stdout, stderr).
        Если check=True и returncode != 0 — выбрасывает CalledProcessError.
        """
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if check and result.returncode != 0:
            raise subprocess.CalledProcessError(
                result.returncode,
                result.args,
                output=result.stdout,
                stderr=result.stderr,
            )
        return result.returncode, result.stdout, result.stderr

    def get_active_interface(self):
        """
        Возвращает имя активного интерфейса WireGuard (awg) или None, если нет.
        """
        try:
            rc, out, err = self._run_cmd(["sudo", "awg", "show"], check=False)
            if rc != 0:
                return None
            for line in out.splitlines():
                if line.startswith("interface:"):
                    iface = line.split(":", 1)[1].strip()
                    return iface
        except Exception:
            # В GUI ошибку обработает вызывающий код
            return None
        return None

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

    def connect_vpn(self, config_name: str, force_disconnect=False) -> bool:
        """
        Подключается к WireGuard конфигурации.

        :param config_name: имя конфига без .conf (например, 'office')
        :param force_disconnect: если True — автоматически отключает активный интерфейс.
                                Если False и есть активный интерфейс — выбрасывает RuntimeError.
        :return: True при успехе.
        :raises: RuntimeError, если нельзя подключиться (нет конфига, есть активный интерфейс и force_disconnect=False, или awg-quick упал).
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))

        config_path = os.path.join(base_dir, self.config_folder, f"{config_name}.conf")

        if not os.path.exists(config_path):
            raise RuntimeError(f"Конфиг не найден: {config_path}")

        active_iface = self.get_active_interface()
        if active_iface is not None:
            if force_disconnect:
                # Сначала отключаем старое соединение
                self.disconnect_vpn()
            else:
                raise RuntimeError(
                    f"Есть активное соединение на интерфейсе '{active_iface}'. "
                    "Отключите его или вызовите connect_vpn с force_disconnect=True."
                )

        # Подключаемся
        self._run_cmd(["sudo", "awg-quick", "up", str(config_path)], check=True)
        print(self.show_status())

        return True

    def disconnect_vpn(self):
        """
        Отключает активный WireGuard интерфейс.
        Возвращает True при успехе, False если интерфейса не было,
        и выбрасывает исключение при ошибке выполнения команды.
        """
        active_iface = self.get_active_interface()
        if active_iface is None:
            return False

        self._run_cmd(["sudo", "ip", "link", "delete", active_iface], check=True)

        print(self.show_status())
        return True

    def _extract_field(self, lines, prefix):
        for line in lines:
            if line.startswith(prefix):
                # берём всё после префикса и обрезаем пробелы
                return line[len(prefix) :].strip()
        return None

    def show_status(self) -> Dict[str, Any]:
        """
        Возвращает статус активного WireGuard соединения в виде словаря.
        Если соединения нет — возвращает словарь с флагом success=False.
        """
        active_iface = self.get_active_interface()
        if active_iface is None:
            return {
                "success": False,
                "message": "Нет активных VPN‑соединений",
                "interface": None,
            }

        # Получаем детали по интерфейсу
        rc, out, err = self._run_cmd(["sudo", "awg", "show", active_iface], check=False)
        if rc != 0:
            return {
                "success": False,
                "message": f"Не удалось получить детали интерфейса: {err}",
                "interface": active_iface,
            }

        lines = out.splitlines()

        endpoint = self._extract_field(lines, "endpoint:")
        handshake = self._extract_field(lines, "latest handshake:")
        transfer = self._extract_field(lines, "transfer:")

        curl_result = subprocess.run(
            ["curl", "-4", "-s", "ifconfig.me"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )

        ip_rc = curl_result.returncode
        ip_out = curl_result.stdout
        current_ip = ip_out.strip() if ip_rc == 0 else "недоступен"

        return {
            "success": True,
            "message": "Активное соединение найдено",
            "interface": active_iface,
            "endpoint": endpoint,
            "handshake": handshake,
            "transfer": transfer,
            "current_ip": current_ip,
        }
