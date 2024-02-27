import json
import subprocess
import os
from functions.helpers import power_on

fp = "config.json"

# Open and read the config.json file:
with open(fp, 'r') as config_file:
    config_data = json.load(config_file)

#hash_init(config_data)
c = 18
power_on(c, ON=True)
ex = "BU_1"
#subprocess.run(["sudo", "mkdir", f"/media/{ex}"])
cmd = f"lsblk -o LABEL,UUID | grep \"{ex}\" | awk '{{print $2}}'"
x = subprocess.run(cmd, shell=True, capture_output=True, text=True)
output_string = x.stdout.strip().replace('"', '')
print(output_string)
#lsblk -o PATH,UUID | grep "BU_1"


#sudo mount -U <UUID> /mnt/mydrive