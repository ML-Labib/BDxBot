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
                "players": {
                    "captain": {"name": team_data["captain"], "role_given": False},
                    "player_2": {"name": team_data["player_2"], "role_given": False},
                    "player_3": {"name": team_data["player_3"], "role_given": False},
                    "player_4": {"name": team_data["player_4"], "role_given": False},
                    "player_5": {"name": team_data["player_5"], "role_given": False},
                    "player_6": {"name": team_data["player_6"], "role_given": False},
                }
            }
        self.profile["teams"] = teams
        utils.write_json_file(self.profile_path, self.profile)
        return

    def get_team(self, team_name: str) -> dict | None:
        return self.profile["teams"].get(team_name, None)
    
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
                player_info["name"] = ""
                player_info["role_given"] = False
                utils.write_json_file(self.profile_path, self.profile)
                return True
        return False   

    def add_team(self, team_name: str, lobby_number: str, p1: str, p2: str, p3: str, p4: str, p5: str, p6: str) -> bool:
        self.profile["teams"][team_name] = {
            "team_name": team_name,
            "lobby_number": lobby_number,
            "players": {
                "captain": {"name": p1, "role_given": False},
                "player_2": {"name": p2, "role_given": False},
                "player_3": {"name": p3, "role_given": False},
                "player_4": {"name": p4, "role_given": False},
                "player_5": {"name": p5, "role_given": False},
                "player_6": {"name": p6, "role_given": False},
            }
        }
        utils.write_json_file(self.profile_path, self.profile)
        return True
    
    
    def add_player(self, team: dict, player_name: str) -> bool:
        for player_key, player_info in team.get("players", {}).items():
            if player_info["name"] == "":
                player_info["name"] = player_name
                player_info["role_given"] = False
                utils.write_json_file(self.profile_path, self.profile)
                return True
        return False
    
    def update_role_given(self, team: dict, player_name: str, value: bool) -> bool:
        for player_key, player_info in team.get("players", {}).items():
            if player_info["name"] == player_name:
                player_info["role_given"] = value
                utils.write_json_file(self.profile_path, self.profile)
                return True
        return False
        

if __name__ == "__main__":
    parser = TournamentParser()

    print("TournamentParser initialized.")