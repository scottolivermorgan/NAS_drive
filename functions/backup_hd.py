import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from library.helpers import (
    activate_logical_volume, 
    mount_logical_volume,
    load_config_file,
    stop_all_docker_containers,
    execute_rsync
    )

if __name__ == "__main__":

    # Load config
    config = load_config_file("../config/config.yml")

    # Activate logical volume
    activate_logical_volume(
        config["backup_volume_group"],
        config["backup_logical_volumes"][0]["name"]
        )
    
    # Mount the logival volume
    mount_logical_volume(
        '/media/BU_1',
        config["backup_volume_group"],
        config["backup_logical_volumes"][0]["name"]
        )
    docker_stop = stop_all_docker_containers()
    
    if docker_stop == 0:
        execute_rsync()
    else:
        print("Error stopping docker containers")

