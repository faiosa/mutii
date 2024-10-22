import customtkinter as ctk
from src.numpad import Numpad
from src.settings import Settings


class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("300x400")
        self.root.title("Numpad Application")

        self.numpad = Numpad(self.root, self.open_settings)
        self.numpad.pack(expand=True, fill="both")

        self.settings_window = None

    def open_settings(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = Settings(self.root)
            self.settings_window.grab_set()

    def run(self):
        self.root.mainloop()
