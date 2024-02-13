import json
from helpers import power_on
import time
import subprocess
import RPi.GPIO as GPIO
import os

def backup_HD(config_data):
    
    print("Closing airgap")

    for object in config_data['HD_map']:
        # get drive mapping details:
        EXTERNAL_HD = config_data["HD_map"][object]["name"]
        back_up_drive_name = hd_name = config_data["HD_map"][object]["back_up_name"]
        signal_pin= hd_name = config_data["HD_map"][object]["GPIO_pin"]
        
        print(f"Mounting {back_up_drive_name} hard drive")
        power_on(signal_pin, ON=True)
        time.sleep(20)
        print(f"Syncing {back_up_drive_name} drive with {EXTERNAL_HD}")

        rsync_cmd = f"rsync -av --log-file=\"/home/{os.getenv('USER')}/NAS_drive/logs/sync_log.log\" /media/{EXTERNAL_HD}/* /media/{os.getenv('USER')}/{back_up_drive_name}"
        print(rsync_cmd)
        sync = subprocess.run(rsync_cmd, shell=True, capture_output=True, text=True)
        
        time.sleep(20)#
        print("Closing airgap")
        power_on(signal_pin, ON=False)

if __name__ == "__main__":
    fp = "/home/scott/NAS_drive/config.json" # change user

    # Open and read the config.json file:
    with open(fp, 'r') as config_file:
        config_data = json.load(config_file)
        
    backup_HD(config_data)