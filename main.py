import json
import subprocess

fp = "config.json"

# Open and read the config.json file:
with open(fp, 'r') as config_file:
    config_data = json.load(config_file)

for object in config_data['HD_map']:

    # get drive mapping details:
    EXTERNAL_HD = config_data["HD_map"][object]["name"]
    back_up_drive_name = hd_name = config_data["HD_map"][object]["back_up_name"]
    signal_pin= hd_name = config_data["HD_map"][object]["GPIO_pin"]

    # Build shell cmd's to pass to subprocesses:

    # Look up UUID of eternal hd and set as an environment variable
    # Note: Commands extract full details of drive from blkid,
    # parse for uuid, strip 'uuid=', strip leading whitespace.
    shell_UUID_str = f"export DRIVE_UUID=$(blkid --match-token LABEL=\"${EXTERNAL_HD}\" | grep -o ' UUID=\"[^\"]*' | sed 's/UUID=\"//' | sed 's/^ *//');"

    # Build mount point:
    mount_location_str = f"mkdir /media/{EXTERNAL_HD};"

    # Mount:
    fstab_entry = f"echo \"UUID=${shell_UUID_str}    /media/hardrive1               ntfs    defaults,errors=remount-ro 0       1\" >> /etc/fstab;"
    cmd = shell_UUID_str + mount_location_str + fstab_entry

    # Execute command to mount drive in fstab:
    subprocess.run(cmd)
