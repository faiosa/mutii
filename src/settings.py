import customtkinter as ctk
import keyboard
import screeninfo
from utils.config_utils import save_config, load_config


class Settings(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Settings")
        self.geometry("300x400")

        self.config = load_config()
        self.monitors = self.detect_monitors()
        self.create_widgets()
        self.current_entry = None
        self.pressed_keys = []
        self.recording = False

    def detect_monitors(self):
        monitors = []
        monitors.append("Built-in Monitor")
        for m in screeninfo.get_monitors():
            monitors.append(m.name)
        return monitors

    def create_widgets(self):
        # Monitor selection dropdown
        monitor_label = ctk.CTkLabel(self, text="Select Monitor:")
        monitor_label.pack(pady=10)

        # Ensure a default value is set if monitor_var is None
        default_monitor = "Built-in Monitor"
        self.monitor_var = ctk.StringVar(
            value=self.config.get("monitor", default_monitor)
        )

        # Ensure monitors list includes at least the default monitor
        self.monitors = self.detect_monitors()
        if default_monitor not in self.monitors:
            self.monitors.insert(0, default_monitor)

        monitor_dropdown = ctk.CTkOptionMenu(
            self, variable=self.monitor_var, values=self.monitors
        )
        monitor_dropdown.pack(pady=10)

        # Shortcuts configuration
        shortcuts_label = ctk.CTkLabel(self, text="Configure Shortcuts:")
        shortcuts_label.pack(pady=10)

        self.entries = {}
        for num in range(10):
            self.create_shortcut_entry(num)

        save_button = ctk.CTkButton(self, text="Save", command=self.save_settings)
        save_button.pack(pady=20)

    def create_shortcut_entry(self, num):
        frame = ctk.CTkFrame(self)
        frame.pack(pady=5, fill="x")

        label = ctk.CTkLabel(frame, text=f"Button {num}:")
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame)
        entry.pack(side="right", padx=10)
        entry.insert(0, self.config.get("shortcuts", {}).get(str(num), ""))
        entry.bind("<Button-1>", lambda event, entry=entry: self.start_recording(entry))
        entry.bind("<FocusOut>", self.stop_recording)

        self.entries[num] = entry

    def start_recording(self, entry):
        self.current_entry = entry
        self.recording = True
        self.current_entry.delete(0, "end")
        self.pressed_keys.clear()
        keyboard.on_press(self.on_key_press)
        keyboard.on_release(self.on_key_release)

    def stop_recording(self, event):
        if self.recording:
            self.recording = False
            keyboard.unhook_all()
            shortcut = " + ".join(self.pressed_keys)
            self.current_entry.delete(0, "end")
            self.current_entry.insert(0, shortcut)
            self.config["shortcuts"][
                str(
                    list(self.entries.keys())[
                        list(self.entries.values()).index(self.current_entry)
                    ]
                )
            ] = shortcut
            save_config(self.config)

    def on_key_press(self, event):
        if self.recording:
            key_name = event.name if event.name != "space" else " "
            if key_name not in self.pressed_keys:
                self.pressed_keys.append(key_name)
            shortcut = " + ".join(self.pressed_keys)
            self.current_entry.delete(0, "end")
            self.current_entry.insert(0, shortcut)

    def on_key_release(self, event):
        if self.recording:
            key_name = event.name if event.name != "space" else " "
            if key_name in self.pressed_keys:
                self.pressed_keys.remove(key_name)
            shortcut = " + ".join(self.pressed_keys)
            self.current_entry.delete(0, "end")
            self.current_entry.insert(0, shortcut)

    def save_settings(self):
        self.config["monitor"] = self.monitor_var.get()
        for num, entry in self.entries.items():
            self.config["shortcuts"][str(num)] = entry.get()

        save_config(self.config)
        self.destroy()
