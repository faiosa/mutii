import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/settings.json")


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as file:
            return json.load(file)
    return {"monitor": "Monitor 1", "shortcuts": {}, "positions": {}}


def save_config(config):
    with open(CONFIG_PATH, "w") as file:
        json.dump(config, file, indent=4)
