import json
import os
from helpers import backup_HD

if __name__ == "__main__":
    # Path to hard drives config file.
    fp = f"/home/{os.getenv('SUDO_USER')}/NAS_drive/config.json"

    # Open and read the config.json file:
    with open(fp, "r") as config_file:
        config_data = json.load(config_file)

    # Sync all drives to designated air gapped backups.
    backup_HD(config_data)
