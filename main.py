import json
import subprocess

from functions.helpers import mount_HD_from_config, hash_init

fp = "config.json"

# Open and read the config.json file:
with open(fp, 'r') as config_file:
    config_data = json.load(config_file)

# Prompt and read user options:
UN = input("Enter current user name? ")
nc_option = input("Install Next Cloud y/n? ")
ext_hd = input("Attach external Hard drive? y/n? ")
ag_bu = input("Configure air gapped backup y/n? ")
shutdown_switch = input("Configure shutdown switch y/n? ")
plex = input("Install Plex server y/n? ")

env = {"UN": UN}

if nc_option == 'y':
    env["NC_USER"] = input("Create nextcloud user: ")
    env["NC_PASSWORD"] = input("Set nextcloud user password: ")

    print("Installing nextcloud dependancies.")
    subprocess.run(["sudo", "sh", "NAS_drive/scripts/nextcloud/nextcloud-dependancies.sh"])
    subprocess.run(["sudo", "sh", "NAS_drive/scripts/nextcloud/nextcloud-installation.sh"], env=env)
    subprocess.run(["sudo", "sh", "NAS_drive/scripts/nextcloud/nextcloud-setup.sh"], env=env)

if ext_hd == 'y':
    EXTERNAL_HD, back_up_drive_name, signal_pin = mount_HD_from_config(config_data)
    dummy = input("enable external storage via nextcloud GUI, type y when enabled.")

if ag_bu == 'y':
    hash_init(config_data)
    subprocess.run(["sudo", "sh", "NAS_drive/scripts/backup_drive/schedule-backup.sh"], env=env)

if shutdown_switch == 'y':
    subprocess.run(["sudo", "sh", "NAS_drive/scripts/shutdown_switch/shutdown.sh"])

if plex == 'y':
    subprocess.run(["sudo", "sh", "NAS_drive/scripts/plex/plex-installation.sh"])
    subprocess.run(["sudo", "sh", "NAS_drive/scripts/plex/mv_meta_loc.sh"])

subprocess.run(["yes", "|", "sudo", "sh", "NAS_drive/scripts/harden_security/auto_patch.sh"])
subprocess.run(["sudo", "reboot"])