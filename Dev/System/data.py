import json

import yaml

from check import check_map, check_settings
from settings import *

class SaveData:
    def __init__(self, filepath: str) -> None:
        with open(filepath, mode = "r") as file:
            self.data = json.load(file)

    def __getitem__(self, key):
        return self.data[key]

    def save_to(self, path, player_status):
        self.data["player-status"] = player_status
        with open(path, "w", encoding = "utf8") as file:
            json.dump(self.data, file, indent = 4)
        print("save data to {}".format(path))

class MapData:
    def __init__(self, filepath: str) -> None:
        with open(filepath, mode = "r") as file:
            self.data = json.load(file)
        check_map(self.data)

    def __getitem__(self, key):
        return self.data[key]

class SettingData:
    def __init__(self, filepath: str) -> None:
        with open(filepath, mode = "r") as file:
            self.data = json.load(file)
        check_settings(self.data)

    def __getitem__(self, key):
        return self.data[key]
        
    def save_to(self, path = SETTING_FILE_PATH):
        with open(path, mode = "w") as file:
            json.dump(self.data, file, indent = 4)

class ScriptData:
    def __init__(self, filepath: str) -> None:
        with open(filepath, mode = "r", encoding = "utf8") as file:
            self.data = yaml.safe_load(file)
    
    def __getitem__(self, key):
        return self.data[key]
