import json
import subprocess
import os
from functions.helpers import mount_HD_from_config, hash_init

fp = "config.json"

# Open and read the config.json file:
with open(fp, "r") as config_file:
    config_data = json.load(config_file)

# Prompt and read user options:
UN = input("Enter current user name? ")
nc_option = input("Install Next Cloud y/n? ")
ext_hd = input("Attach external Hard drive? y/n? ")
ag_bu = input("Configure air gapped backup y/n? ")
shutdown_switch = input("Configure shutdown switch y/n? ")
plex = input("Install Plex server y/n? ")
if plex == "y":
    data_dir_location = input(
        "Enter meta data location eg: /media/HD_1/Media/metadata: "
    )
    os.environ["PLEX_DATA_LOC"] = data_dir_location
security = input("Harden security settings y/n?")
reboot = input("Reboot after y/n?")

# env = {"UN": UN}
os.environ["UN"] = UN

if nc_option == "y":
    os.environ["NC_USER"] = input("Create nextcloud user: ")
    os.environ["NC_PASSWORD"] = input("Set nextcloud user password: ")

    print("Installing nextcloud dependancies.")
    subprocess.run(["sh", "scripts/nextcloud/nextcloud-dependancies.sh"])
    subprocess.run(["sh", "scripts/nextcloud/nextcloud-installation.sh"])
    subprocess.run(["sh", "scripts/nextcloud/nextcloud-setup.sh"])
    scan_drive = input("Scan external drive (could take hours) y/n?: ")
    if scan_drive == "y":
        scan_cmd = (
            "sudo -u www-data php /var/www/nextcloud/occ files:scan --all --verbose"
        )
        subprocess.run(
            scan_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

if ext_hd == "y":
    print("initialising hard drives")
    drive_mapping = mount_HD_from_config(config_data)
    dummy = input("enable external storage via nextcloud GUI, type y when enabled.")

if ag_bu == "y":
    print("Initialising backup routine")
    initalise_hashes = hash_init(config_data)
    subprocess.run(["sh", "scripts/backup_drive/schedule-backup.sh"])

if shutdown_switch == "y":
    print("Configuring shutdown switch")
    subprocess.run(["sh", "scripts/shutdown_switch/shutdown.sh"])

if plex == "y":
    subprocess.run(["sudo", "sh", "scripts/plex/plex-installation.sh"])
    subprocess.run(["sh", "scripts/plex/mv_meta_loc.sh"])

if security == "y":
    print(" Hardening security")
    # subprocess.run(["yes", "|", "sudo", "sh", "scripts/harden_security/auto_patch.sh"])
    subprocess.run(["sudo", "sh", "scripts/harden_security/auto_patch.sh"])

if reboot == "y":
    subprocess.run(["sudo", "reboot"])
