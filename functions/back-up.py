import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from library.helpers import backup_HD

if __name__ == "__main__":
    # Path to hard drives config file.
    fp = f"/home/{os.getenv('USER')}/NAS_drive/config/config.json"

    # Open and read the config.json file:
    with open(fp, "r") as config_file:
        config_data = json.load(config_file)

    # Sync all drives to designated air gapped backups.
    backup_HD(config_data)
