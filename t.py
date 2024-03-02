import json
import subprocess
import os
from functions.helpers import power_on
import time

fp = "config.json"

# Open and read the config.json file:
with open(fp, 'r') as config_file:
    config_data = json.load(config_file)

#hash_init(config_data)
c = 18
power_on(c, ON=True)
time.sleep(10)
ex = "BU_1"
subprocess.run(["sudo", "mkdir", f"/media/{ex}"])
cmd = f"lsblk -o LABEL,UUID | grep \"{ex}\" | awk '{{print $2}}'"
x = subprocess.run(cmd, shell=True, capture_output=True, text=True)
output_string = x.stdout.strip().replace('"', '')
print("uuid = ",output_string)

z = subprocess.run(["sudo", "mount", "-U", output_string, f"/media/{ex}"])

rsync_cmd = f"sudo rsync -av' /media/HD_1/* /media/{os.getenv('USER')}/BU_1"
sync = subprocess.run(rsync_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
