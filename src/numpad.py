import customtkinter as ctk
from utils.mouse_utils import move_mouse_to_position
from utils.config_utils import load_config


class Numpad(ctk.CTkFrame):
    def __init__(self, master, open_settings_callback):
        super().__init__(master)
        self.open_settings_callback = open_settings_callback

        self.create_numpad_buttons()
        self.create_settings_button()

    def create_numpad_buttons(self):
        for i in range(3):
            for j in range(3):
                number = i * 3 + j + 1
                button = ctk.CTkButton(
                    self,
                    text=str(number),
                    command=lambda num=number: self.on_button_click(num),
                )
                button.grid(row=i, column=j, padx=5, pady=5)

        zero_button = ctk.CTkButton(
            self, text="0", command=lambda: self.on_button_click(0)
        )
        zero_button.grid(row=3, column=1, padx=5, pady=5)

    def create_settings_button(self):
        settings_button = ctk.CTkButton(
            self, text="⚙️", command=self.open_settings_callback
        )
        settings_button.grid(row=4, column=0, padx=5, pady=5, columnspan=3)

    def on_button_click(self, number):
        config = load_config()
        position = config.get("positions", {}).get(str(number), (0, 0))
        move_mouse_to_position(*position)
