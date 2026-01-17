from parser.tournamentParser  import TournamentParser
from parser.configParser import ConfigParser
import sys
from google import sheet
config_parser = ConfigParser()
print(config_parser.show_config())

config_parser.set_vc_category("123456789012345678")
config_parser.set_moss_category("123456789012345679")
config_parser.set_authorized_cleaner_1(111111111111111111)
config_parser.set_authorized_cleaner_2(222222222222222222)

print(config_parser.show_config())

