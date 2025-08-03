import os
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from library.helpers import (
    activate_logical_volume, 
    mount_logical_volume,
    load_config_file,
    execute_rsync
    )

def run_bash_script(script_path):
    """Function to run the bash script."""
    try:
        # Execute the bash script using subprocess
        result = subprocess.run(['bash', script_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # If successful, return 0 (success code)
        print(result.stdout.decode())  # Optionally print the output of the script
        return 0
    except subprocess.CalledProcessError as e:
        # If there's an error, print the error and return non-zero code
        print(f"Error executing script: {e.stderr.decode()}")
        return 1


if __name__ == "__main__":

    # Load config
    print("loading config")
    config = load_config_file("../config/config.yml")

    # Activate logical volume
    print("activating logical volumes")
    activate_logical_volume(
        config["backup_volume_group"],
        config["backup_logical_volumes"][0]["name"]
        )
    
    # Mount the logival volume
    print("mounting logical volumnes")
    mount_logical_volume(
        '/media/BU_1',
        config["backup_volume_group"],
        config["backup_logical_volumes"][0]["name"]
        )
    
    script_path = './docker_compose_stop.sh'  # Path to your bash script
    docker_stop = run_bash_script(script_path)
    
    if docker_stop == 0:
        print("containers stopped sucsessfully - executing rsync")
        execute_rsync()
    else:
        print("Error stopping docker containers")

