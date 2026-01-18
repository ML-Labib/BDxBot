from parser.tournamentParser  import TournamentParser
from parser.configParser import ConfigParser
import sys
from google import sheet
t_parser = TournamentParser()

print(t_parser.teams_status())

