import re
def mount_HD_from_config():
    # Define a regular expression pattern to match UUID="..."
    pattern = r'UUID=([a-f0-9-]+)'
    with open('/etc/fstab','r') as f:
        data = f.readlines()
    for line in data:
        match = re.search(pattern, line)
        if match:
            # Extract the UUID from the matched group
            uuid = match.group(1)
            print("UUID:", uuid)
        else:
            print("UUID not found in the input string.")
    

mount_HD_from_config()