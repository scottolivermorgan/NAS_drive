import json
import subprocess
import os
from functions.helpers import mount_HD_from_config, hash_init

fp = "config.json"

# Open and read the config.json file:
with open(fp, 'r') as config_file:
    config_data = json.load(config_file)

hash_init(config_data)