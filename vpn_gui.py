import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from vpn_controller import VPNController


class VPNGUI():
    """GUI

    Атрибуты:
        _window (tk): точка входа в GUI.
    """
    _window: tk
    _vpn_controller: VPNController
    _config_folder_var: tk

    def __init__(self, vpn_controller: VPNController):
        """Инициализируем графический интерфейс и устанавливаем vpn_controller

        Args:
            vpn_controller (VPNController): менеджер управления конфигурациями
        """
        if not isinstance(vpn_controller, VPNController):
            raise TypeError(
                f"vpn_controller должен быть экземпляром VPNController, "
                f"получено: {type(vpn_controller).__name__}"
            )
        self._vpn_controller = vpn_controller

        self._window = tk.Tk()
        self._window.title("awg-quick gui")
        self._window.geometry("300x500")
        self._window.resizable(width=False, height=False)

        self._main_widget()

    def _main_widget(self):
        """Создание основного виджета-контейнера"""
        main_frame = ttk.Frame(self._window)
        main_frame.pack(fill="both", expand=1)

        config_frame = ttk.LabelFrame(main_frame, text="Папка с конфигами", padding="5")
        config_frame.pack(fill=tk.X, pady=5)
        
        self._config_folder_var = tk.StringVar(value=self._vpn_controller.config_folder)
        ttk.Label(config_frame, textvariable=self._config_folder_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(config_frame, text="Изменить", command=self._change_config_folder).pack(side=tk.RIGHT, padx=5)
        ttk.Button(config_frame, text="Сбросить", command=self._reset_config_folder).pack(side=tk.RIGHT)

    def _reset_config_folder(self):
        pass

    def _change_config_folder(self):
        pass
    def run(self):
        self._window.mainloop()