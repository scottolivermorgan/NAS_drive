import re
def mount_HD_from_config():
    # Define a regular expression pattern to match UUID="..."

    t = "/dev/sdb2: LABEL=\"HD_1\" BLOCK_SIZE=\"512\" UUID=\"C41E05971E0583A0\" TYPE=\"ntfs\" PARTLABEL=\"Basic data partition\" PARTUUID=\"901cd3b6-9bb1-439a-b3c3-f91c42c6319b\""
    label_pattern = r'LABEL="(.*?)"'
    pattern = r'UUID=([a-f0-9-]+)'
    bla = re.search(label_pattern, t)
    print(bla.group(1))
    #with open('/etc/fstab','r') as f:
    #    data = f.readlines()
    #for line in data:
    #    match = re.search(pattern, line)
    #    if match:
    #        # Extract the UUID from the matched group
    #        uuid = match.group(1)
    #        print("UUID:", uuid)
    #    else:
     #       print("UUID not found in the input string.")
    

mount_HD_from_config()