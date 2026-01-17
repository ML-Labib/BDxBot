from parser.TournamentParser  import TournamentParser
import sys
from google import sheet
tournament_parser = TournamentParser()
# reader = sheet.get_csv_form_sheet("https://docs.google.com/spreadsheets/d/1h6f61MqmR8N0YuPbf1hgfe2vR_LjoI6WereUupiD7Qk/edit?gid=0#gid=0")
# tournament_parser.new_profile(reader[1])
team = tournament_parser.get_team("Test team 1")
if team:
    status = tournament_parser.remove_player(team, "BB")
    if status:
        print("Player removed successfully.")
    else:
        print("Player not found.")
else:
    print("Team not found.")

team = tournament_parser.get_team("Test team 1")
if team is None:
    print("Team not found for addition.")
    tournament_parser.add_team("Test team 1", "1", "AA", "BB", "CC", "DD", "EE", "FF")
    print("Team added successfully.")
else:
    print("Team already exists.")

tournament_parser.remove_player(team, "CC")

team = tournament_parser.get_team("Test team 1")
if team:
    print("Team found.")
    print(team)
    status3 = tournament_parser.add_player(team, "New Player")
else:
    print("Team not found.")
    status3 = False
if status3:
    print("Player added successfully.")
else:
    print("No empty slot available for new player.")
print(team)