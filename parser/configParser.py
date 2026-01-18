import pathlib
import os
from utils import utils
import csv

class ConfigParser:
    def __init__(self) -> None:
        self.base_path = pathlib.Path(__file__).parent.parent
        self.config_path = os.path.join(self.base_path, 'database', 'config.json')
        self.config = utils.read_json_file(self.config_path)


    def show_config(self) -> str:
        text = f"Current Configuration:\nVC Category: <#{self.config["vc_category_id"]}>\nMOSS Category: <#{self.config["moss_category_id"]}>\nAuthorized Cleaner 1: <@{self.config["authorized_cleaner_1"]}>\nAuthorized Cleaner 2: <@{self.config["authorized_cleaner_2"]}>"
        return text
    
    def set_vc_category(self, category_id: str) -> None:
        self.config["vc_category_id"] = category_id
        utils.write_json_file(self.config_path, self.config)
        return
    
    def get_vc_category(self):
        return self.config["vc_category_id"]

    
    def set_moss_category(self, category_id: str) -> None:
        self.config["moss_category_id"] = category_id
        utils.write_json_file(self.config_path, self.config)
        return
    
    def get_moss_category(self):
        return self.config["moss_category_id"]
    
    def set_authorized_cleaner_1(self, user_id: int) -> bool:
        if user_id == self.config["authorized_cleaner_2"]:
            return False
        self.config["authorized_cleaner_1"] = user_id
        utils.write_json_file(self.config_path, self.config)
        return True
    
    def set_authorized_cleaner_2(self, user_id: int) -> bool:
        if user_id == self.config["authorized_cleaner_1"]:
            return False
        self.config["authorized_cleaner_2"] = user_id
        utils.write_json_file(self.config_path, self.config)
        return True
    
    def get_authorized_cleaner_1(self):
        return self.config["authorized_cleaner_1"]
    
    def get_authorized_cleaner_2(self):
        return self.config["authorized_cleaner_2"]

    def get_authorized(self):
        return self.config["authorized"]
    
    def append_authorized(self, user_id):
        auth = self.get_authorized()
        auth.append(user_id)
        utils.write_json_file(self.config_path, self.config)

    def reset_auth(self):
        self.config["authorized"] = []
        utils.write_json_file(self.config_path, self.config)

    def reset_config(self) -> None:
        self.config = {
            "vc_category_id": "",
            "moss_category_id": "",
            "authorized_cleaner_1": 0,
            "authorized_cleaner_2": 0,
            "authorized": []
        }
        utils.write_json_file(self.config_path, self.config)
        return  
    
if __name__ == "__main":
    p = ConfigParser()
    print(p.config )
