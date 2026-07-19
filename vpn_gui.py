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
    _config_folder_var: tk.StringVar
    _config_listbox: tk.Listbox
    _status_var: tk.StringVar
    _connect_btn: tk.Button
    _disconnect_btn: tk.Button
    _status_bar: tk.Label
    _status_var_label: tk.Label

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
        self._refresh_config_list()

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

        self._config_listbox = tk.Listbox(configs_frame, yscrollcommand=scrollbar.set)
        self._config_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self._config_listbox.yview)

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
        self._status_var = tk.StringVar(value="Отключено")
        self._status_var_label = ttk.Label(
            status_frame, textvariable=self._status_var, foreground="red"
        )
        self._status_var_label.pack(side=tk.LEFT, padx=5)

        # Кнопки подключения
        btn_frame = ttk.Frame(vpn_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        self._connect_btn = ttk.Button(
            btn_frame, text="Подключиться", command=self._connect_vpn
        )
        self._connect_btn.pack(side=tk.LEFT, padx=5)

        self._disconnect_btn = ttk.Button(
            btn_frame,
            text="Отключиться",
            command=self._disconnect_vpn,
            # state=tk.DISABLED,
        )
        self._disconnect_btn.pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame, text="Проверить соединение", command=self._test_connection
        ).pack(side=tk.LEFT, padx=5)

        # Строка статуса
        self._status_bar = ttk.Label(
            self._window, text="Готов", relief=tk.SUNKEN, anchor=tk.W
        )
        self._status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _reset_config_folder(self):
        """Сбросить теукщую папку с конфигами на дефолтную"""
        new_dir = self._vpn_controller.reset_config_folder()
        if new_dir:
            self._config_folder_var.set(new_dir)
            self._refresh_config_list()
            messagebox.showinfo("Успех", f"Папка конфигов изменена на:\n{new_dir}")
            self._status_bar.config(text=f"Папка изменена: {new_dir}")

    def _change_config_folder(self):
        """Сменить папку с конфигами"""
        new_dir = filedialog.askdirectory(title="Выберите папку с конфигами VPN")
        if new_dir:
            if self._vpn_controller.change_config_folder(new_dir):
                self._config_folder_var.set(self._vpn_controller.config_folder)
                self._refresh_config_list()
                messagebox.showinfo("Успех", f"Папка конфигов изменена на:\n{new_dir}")
                self._status_bar.config(text=f"Папка изменена: {new_dir}")
            else:
                messagebox.showerror("Ошибка", "Не удалось изменить папку конфигов")

    def _add_config(self):
        pass

    def _delete_config(self):
        pass

    def _refresh_config_list(self):
        """Обновляем список конфигов в указанной папке"""
        self._config_listbox.delete(0, tk.END)
        configs = self._vpn_controller.get_list_config_file()

        if configs:
            for config in configs:
                self._config_listbox.insert(tk.END, config.stem)

    def _connect_vpn(self):
        selection = self._config_listbox.curselection()
        if selection:
            idx = selection[0]
            config_name = self._config_listbox.get(idx)

            if self._vpn_controller.connect_vpn(config_name):
                self._status_var.set("Подключено")
                status_label = self._status_var_label
                status_label.configure(foreground="green")
                self._connect_btn.config(state=tk.DISABLED)
                self._disconnect_btn.config(state=tk.NORMAL)
                self._status_bar.config(text=f"Подключено к {config_name}")
                # messagebox.showinfo("Успех", f"Подключено к {config_name}")

    def _disconnect_vpn(self):
        self._status_bar.config(text="Отключение...")

        if self._vpn_controller.disconnect_vpn():
            self._status_var.set("Отключено")
            status_label = self._status_var_label
            status_label.configure(foreground="red")
            self._connect_btn.config(state=tk.NORMAL)
            # self.disconnect_btn.config(state=tk.DISABLED)
            self._status_bar.config(text="Отключено от VPN")

    def _test_connection(self):
        print(self._vpn_controller.show_status())

    def run(self):
        self._window.mainloop()
