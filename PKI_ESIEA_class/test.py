from argparse import ArgumentParser, Namespace
from distutils.command.config import config
import json
def parse_args()-> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", help="Config file", required=True, dest="config", nargs='+')
    return parser.parse_args()
            
                       
args = parse_args()
configfile = args.config


with open("Config_CA.json", "r") as file :
    config = json.loads(file.read())
print(str(config))

with open("Config_RA.json", "r") as file :
    config2 = json.loads(file.read())
print(str(config2))