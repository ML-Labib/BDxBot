import pathlib
import os
from utils import utils
import csv

class TournamentParser:
    def __init__(self) -> None:
        self.base_path = pathlib.Path(__file__).parent.parent
        self.profile_path = os.path.join(self.base_path, 'database', 'profile.json')
        self.profile = utils.read_json_file(self.profile_path)

    def new_profile(self, reader: csv.DictReader) -> None:
        teams: dict[str, list[str]] = {}
        for team_data in reader:
            teams[team_data["team_name"]] = {
                "team_name": team_data["team_name"],
                "lobby_number": team_data["lobby_number"],
                "vc_id": "",
                "moss_id": "",
                "role_id": "",
                "players": {
                    "captain": {"name": team_data["captain"], "role_given": False, "notified": False},
                    "player_2": {"name": team_data["player_2"], "role_given": False, "notified": False},
                    "player_3": {"name": team_data["player_3"], "role_given": False, "notified": False},
                    "player_4": {"name": team_data["player_4"], "role_given": False, "notified": False},
                    "player_5": {"name": team_data["player_5"], "role_given": False, "notified": False},
                    "player_6": {"name": team_data["player_6"], "role_given": False, "notified": False},
                }
            }
        self.profile["teams"] = teams
        utils.write_json_file(self.profile_path, self.profile)
        return

    def get_team(self, team_name: str) -> dict | None:
        return self.profile["teams"].get(team_name, None)
    

    def get_all_teams(self) -> dict:
        return self.profile["teams"]


    def remove_team(self, team_name: str) -> bool:
        team = self.get_team(team_name)
        if team:
            del self.profile["teams"][team_name]
            utils.write_json_file(self.profile_path, self.profile)
            return True
        return False
    
    def remove_player(self, team: dict, player_name: str) -> bool:
        players = team.get("players", {})
        for player_key, player_info in players.items():
            if player_info["name"] == player_name:
                player_info["name"] = "x"
                player_info["role_given"] = False
                player_info["notified"] = False
                utils.write_json_file(self.profile_path, self.profile)
                return True
        return False   

    def add_team(self, team_name: str, lobby_number: str, p1: str, p2: str, p3: str, p4: str, p5: str, p6: str) -> bool:
        self.profile["teams"][team_name] = {
            "team_name": team_name,
            "lobby_number": lobby_number,
            "vc_id": "",
            "moss_id": "",
            "role_id": "",
            "players": {
                "captain": {"name": p1, "role_given": False, "notified": False},
                "player_2": {"name": p2, "role_given": False, "notified": False},
                "player_3": {"name": p3, "role_given": False, "notified": False},
                "player_4": {"name": p4, "role_given": False, "notified": False},
                "player_5": {"name": p5, "role_given": False, "notified": False},
                "player_6": {"name": p6, "role_given": False, "notified": False},
            }
        }
        utils.write_json_file(self.profile_path, self.profile)
        return True
    
    
    def add_player(self, team: dict, player_name: str) -> bool:
        for player_key, player_info in team.get("players", {}).items():
            if player_info["name"] == "" or player_info["name"] == "x":
                player_info["name"] = player_name
                player_info["role_given"] = False
                utils.write_json_file(self.profile_path, self.profile)
                return True
        return False
    
    
    def team_status(self, team: dict) -> str:
        p = "Players:"
        r = "Role Given"
        text = f"{team['lobby_number']}. **{team['team_name']}**:\n"
        text += f"{p:40} {r}\n"
        counter = 1
        for player_key, player_info in team["players"].items():
            if player_info["name"] == "" or player_info["name"] == "x":
                continue
            role_status = "✅" if player_info["role_given"] else "❌"
            text += f"{counter}. {player_info['name']:40} {role_status}\n"
            counter += 1
        return text
    
    def all_teams_status(self) -> str:
        text = ""
        for team_name, team_info in self.profile["teams"].items():
            text += self.team_status(team_info)
        return text
    
    def set_vc_id(self, team: dict, vc_id: str):
        team["vc_id"] = vc_id
        utils.write_json_file(self.profile_path, self.profile)
        
    
    def set_moss_id(self, team: dict, moss_id):
        team["moss_id"] = moss_id
        utils.write_json_file(self.profile_path, self.profile)

    def set_role_id(self, team:str, role_id):
        team["role_id"] = role_id
        utils.write_json_file(self.profile_path, self.profile)
        
    def update_role_given(self, team: dict, player_name: str, value: bool) -> bool:
        for player_key, player_info in team.get("players", {}).items():
            if player_info["name"] == player_name:
                player_info["role_given"] = value
                utils.write_json_file(self.profile_path, self.profile)
                return True
        return False
    
    def update_notified(self, player_info: dict, value: bool) -> bool:
        player_info["notified"] = value
        utils.write_json_file(self.profile_path, self.profile)
        return True

    
    def is_role_given(self, team: dict, player_name: str) -> bool | None:
        for player_key, player_info in team.get("players", {}).items():
            if player_info["name"] == player_name:
                return player_info["role_given"]
        return False
    
    def reset_teams(self):
        self.profile["teams"] = {}
        utils.write_json_file(self.profile_path, self.profile)
        

if __name__ == "__main__":
    parser = TournamentParser()

    print("TournamentParser initialized.")