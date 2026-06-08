import tkinter as tk


class VPNGUI():
    """GUI

    Атрибуты:
        _window (tk): точка входа в GUI.
    """
    _window: tk

    def __init__(self):
        self._window = tk.Tk()
        self._window.title("awg-quick gui")
        self._window.geometry("300x200")
        self._window.resizable(width=False, height=False)

    def run(self):
        self._window.mainloop()