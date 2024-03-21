import json
import os
from library.helpers import mount_HD_from_config, hash_init

if __name__ == "__main__":
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate to the config directory
    config_dir = os.path.join(current_dir, '..', 'config')

    # Open the config.json file
    config_path = os.path.join(config_dir, 'config.json')

    # Open and read the config.json file:
    with open(config_path, "r") as config_file:
        config_data = json.load(config_file)

    drive_mapping = mount_HD_from_config(config_data)
    initalise_hashes = hash_init(config_data)
