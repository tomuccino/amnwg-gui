import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from vpn_controller import VPNController


class VPNGUI:
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
        self._window.geometry("500x600")
        self._window.resizable(width=False, height=False)

        self._main_widget()

    def _main_widget(self):
        """Создание основного виджета-контейнера"""
        main_frame = ttk.Frame(self._window)
        main_frame.pack(fill="both", expand=1)

        config_frame = ttk.LabelFrame(main_frame, text="Папка с конфигами", padding="5")
        config_frame.pack(fill=tk.X, pady=5)

        self._config_folder_var = tk.StringVar(value=self._vpn_controller.config_folder)
        ttk.Label(config_frame, textvariable=self._config_folder_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True
        )
        ttk.Button(
            config_frame, text="Изменить", command=self._change_config_folder
        ).pack(side=tk.RIGHT, padx=5)
        ttk.Button(
            config_frame, text="Сбросить", command=self._reset_config_folder
        ).pack(side=tk.RIGHT)

        # Список конфигов
        configs_frame = ttk.LabelFrame(
            main_frame, text="Доступные конфиги", padding="5"
        )
        configs_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Список
        scrollbar = ttk.Scrollbar(configs_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.config_listbox = tk.Listbox(configs_frame, yscrollcommand=scrollbar.set)
        self.config_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.config_listbox.yview)

        # Кнопки управления конфигами
        config_btn_frame = ttk.Frame(configs_frame)
        config_btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            config_btn_frame, text="Добавить конфиг", command=self._add_config
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            config_btn_frame, text="Удалить конфиг", command=self._delete_config
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            config_btn_frame, text="Обновить список", command=self._refresh_config_list
        ).pack(side=tk.LEFT, padx=2)

        # Панель управления VPN
        vpn_frame = ttk.LabelFrame(main_frame, text="Управление VPN", padding="5")
        vpn_frame.pack(fill=tk.X, pady=5)

        # Статус
        status_frame = ttk.Frame(vpn_frame)
        status_frame.pack(fill=tk.X, pady=5)

        ttk.Label(status_frame, text="Статус:").pack(side=tk.LEFT)
        self.status_var = tk.StringVar(value="Отключено")
        ttk.Label(status_frame, textvariable=self.status_var, foreground="red").pack(
            side=tk.LEFT, padx=5
        )

        # Кнопки подключения
        btn_frame = ttk.Frame(vpn_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        self.connect_btn = ttk.Button(
            btn_frame, text="Подключиться", command=self._connect_vpn
        )
        self.connect_btn.pack(side=tk.LEFT, padx=5)

        self.disconnect_btn = ttk.Button(
            btn_frame,
            text="Отключиться",
            command=self._disconnect_vpn,
            state=tk.DISABLED,
        )
        self.disconnect_btn.pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame, text="Проверить соединение", command=self._test_connection
        ).pack(side=tk.LEFT, padx=5)

        # Строка статуса
        self.status_bar = ttk.Label(
            self._window, text="Готов", relief=tk.SUNKEN, anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _reset_config_folder(self):
        pass

    def _change_config_folder(self):
        pass

    def _add_config(self):
        pass

    def _delete_config(self):
        pass

    def _refresh_config_list(self):
        pass

    def _connect_vpn(self):
        pass

    def _disconnect_vpn(self):
        pass

    def _test_connection(self):
        pass

    def run(self):
        self._window.mainloop()
