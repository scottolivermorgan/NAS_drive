import hashlib
import json
import subprocess
#import RPi.GPIO as GPIO
from datetime import datetime
import random
import os
from dotenv import load_dotenv
import re

def power_on(RELAY_CHANNEL, ON) -> None:
    """
    Turns on the power by setting the GPIO output to high for the specified relay channel.

    This function uses the GPIO library to control a relay channel, turning it on by setting the
    corresponding GPIO output to high.

    Note:
    Make sure to initialize the GPIO setup before calling this function.

    Example:
    ```python
    # Set up GPIO (assumed to be done before calling power_on)
    GPIO.setup(RELAY_CHANNEL, GPIO.OUT)

    # Turn on the power
    power_on()
    ```

    Raises:
        Any exceptions raised by the GPIO library during the output setting.

    Global Constants:
        - RELAY_CHANNEL: The GPIO channel connected to the relay.

    """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_CHANNEL, GPIO.OUT)
    GPIO.output(RELAY_CHANNEL, GPIO.HIGH)
    if ON is True:
        GPIO.output(RELAY_CHANNEL, GPIO.HIGH)
        return 1
    else:
        GPIO.output(RELAY_CHANNEL, GPIO.LOW)
        return 0


def create_hash_file(paths):
    """
    Create a hash file for the current datetime and save it in the specified paths.

    Parameters:
    - paths (List[str]): A list of file paths where the hash file will be saved.

    Returns:
    - List[str]: A list of file names corresponding to the saved hash files.

    Example:
    ```python
    paths = ['/path/to/directory1', '/path/to/directory2']
    filenames = create_hash_file(paths)
    ```

    The function creates a hash file for the current datetime using SHA-256.
    The hash is written to a text file, and the file is saved in the specified
    directories. The file name format is 'hash_YYYY-MM-DD_HH-MM-SS.txt'.
    If multiple paths are provided, the hash is written with an offset using 
    the `hash_offset` function to ensure uniqueness across files.
    """
    # Get the current datetime
    current_datetime = datetime.now()

    # Convert the datetime to a string
    datetime_str = str(current_datetime)

    # Calculate the hash of the datetime string using SHA-256
    hash_object = hashlib.sha256(datetime_str.encode())
    hash_hex = hash_object.hexdigest()

    # Create a text file and write the hash to it
    fn = []
    for path in paths:
        file_name = f"{path}/hash_{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        fn.append(file_name)
        with open(file_name, 'w') as file:
            if path == paths[-1]:
                offset_hash = hash_offset(hash_hex, reset=False)
                file.write(offset_hash)
            else:
                file.write(hash_hex)

    print(f"Hash saved to {file_name}")
    return fn

def select_random_location(folder_path):
    """
    Selects a random file path within the specified folder and its subfolders.

    Args:
        folder_path (str): The path to the folder for which a random file path will be selected.

    Returns:
        str or None: A randomly selected file path if files are found, or None if
        the folder is empty.

    Raises:
        ValueError: If the provided folder_path is not a valid directory.

    Example:
        >>> pre_sync_hash_verification("/path/to/folder")
        '/path/to/folder/random_file.txt'

    Note:
        This function walks through the specified folder and its subfolders to collect file paths.
        It only logs the last directory if a file is present in that directory.

    """
    # Create a list to store all file paths within the folder and its subfolders
    all_files = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root)
            all_files.append(file_path)

    # Select a random file path
    random_location = random.choice(all_files)
    return random_location

def pre_sync_hash_verification() -> bool:
    """
    Perform pre-synchronization hash verification between a source and destination hash.

    This function reads hash values from the source and destination files,
    adjusts the destination hash using the `hash_offset` function, and compares
    the result with the source hash.

    Returns:
        bool: True if the source hash matches the adjusted destination hash, False otherwise.
    """
    # Set enviroment variables
    load_dotenv()
    src = os.getenv("SRC_VALIDATION_HASH_LOC")
    dst = os.getenv("DST_VALIDATION_HASH_LOC")

    with open(src, 'r', encoding="utf8") as f:
        src_hash = f.readlines()

    with open(dst, 'r', encoding="utf8") as f:
        dst_hash = f.readlines()
        dst_hash = hash_offset(dst_hash[0], reset=True)

    if src_hash[0] == dst_hash:
        return True
    return False

def hash_offset(hash_key: str, reset: bool) -> str:
    """
    Computes an offset for each character in the input hash string based on the 'reset' flag.

    Args:
        hash (str): The input hash string for which the offset is computed.
        reset (bool): A flag indicating whether to reset the offset (True) or increment it (False).

    Returns:
        str: The resulting offset string, where each character is adjusted based
        on the 'reset' flag.
        
    Example:
        >>> hash_offset("abc123", True)
        '`ba098'
        
        >>> hash_offset("xyz789", False)
        'yz{890'
    """
    offset = ''
    for i in hash_key:
        if reset:
            offset += (chr(ord(i) - 1))
        else:
            offset += (chr(ord(i) + 1))

    return offset

def mount_HD_from_config(config_data):
    drive_mapping = {}
    for object in config_data['HD_map']:
        # get drive mapping details:
        EXTERNAL_HD = config_data["HD_map"][object]["name"]
        print(f"Found {EXTERNAL_HD}")
        back_up_drive_name = hd_name = config_data["HD_map"][object]["back_up_name"]
        signal_pin= hd_name = config_data["HD_map"][object]["GPIO_pin"]

        # Build shell cmd's to pass to subprocesses:

        # Look up UUID of eternal hd and set as an environment variable
        # Note: Commands extract full details of drive from blkid,
        # parse for uuid, strip 'uuid=', strip leading whitespace.
        #UUID_cmd = f"blkid --match-token LABEL=\"${EXTERNAL_HD}\" | grep -o ' UUID=\"[^\"]*' | sed 's/UUID=\"//' | sed 's/^ *//');"
        #UUID_cmd = ["blkid", "--match-token", f"\"LABEL=\"${EXTERNAL_HD}\"",
        #             "|", "grep", "-o", "\' UUID=\"[^\"]*\'",
        #               "|", "sed", "\'s/UUID=\"//'", "|", "sed",
        #                 "\'s/^ *//');\""]
        #UUID = subprocess.run(UUID_cmd)
        """
        UUID_cmd = [
                    "blkid",
                    "--match-token",
                    f"LABEL={EXTERNAL_HD}",
                    "|",
                    "grep",
                    "-o",
                    ' UUID="[^\"]*"',
                    "|",
                    "sed",
                    's/UUID=//',
                    "|",
                    "sed",
                    's/^ *//'
                ]

        UUID = check_output(UUID_cmd)
        print("uuid = ", UUID)
        print("type", type(UUID))
        #print(UUID[])
        #UUID_output = UUID.communicate()[0].decode("utf-8").strip()
        
        UUID_cmd = [
                    "blkid",
                    "--match-token",
                    f"LABEL={EXTERNAL_HD}",
                    "|",
                    "grep",
                    "-o",
                    ' UUID="[^\"]*"',
                    "|",
                    "sed",
                    's/UUID=//',
                    "|",
                    "sed",
                    's/^ *//'
                ]

        # Use subprocess.Popen to execute the commands and pipe their output
        process1 = subprocess.Popen(UUID_cmd[0:4], stdout=subprocess.PIPE)
        process2 = subprocess.Popen(UUID_cmd[4:8], stdin=process1.stdout, stdout=subprocess.PIPE)
        process3 = subprocess.Popen(UUID_cmd[8:12], stdin=process2.stdout, stdout=subprocess.PIPE)

        # Get the output of the last command in the pipeline
        output, _ = process3.communicate()
        
        # Decode the output to a string
        UUID = output.decode('utf-8').strip()
        """
            # Define a regular expression pattern to match UUID="..."
        label_pattern = r'LABEL="(.*?)"'
        uuid_pattern = r'UUID=([a-f0-9-]+)'
        with open('/etc/fstab','r') as f:
            data = f.readlines()

        for line in data:
            label_filter = re.search(label_pattern, line)

            if label_pattern.group(1) == EXTERNAL_HD:
                match = re.search(uuid_pattern, line)
                UUID = match.group(1)
                print("UUID:", UUID)
            #print('filter', label_filter)
            #print('name', EXTERNAL_HD)
            """
            match = re.search(uuid_pattern, line)
            if match:
                # Extract the UUID from the matched group
                UUID = match.group(1)
                print("UUID:", UUID)
            else:
                print("UUID not found in the input string.")
        """
        #print("uui =", UUID)
        # Build mount point & mount:
        mount_location_str = f"/media/{EXTERNAL_HD}"
        MOUNT_DIR = subprocess.run(["sudo", "mkdir", mount_location_str])

        # Add mount on boot:
        #fstab_cmd = f"echo \"UUID=${UUID}    {mount_location_str}               ntfs    defaults,errors=remount-ro 0       1\" >> /etc/fstab;"
        #fstab_cmd = ["echo", f"UUID=${UUID}    {mount_location_str}               ntfs    defaults,errors=remount-ro 0       1", ">>", "/etc/fstab;"]

        # Execute command to mount drive in fstab:
        #subprocess.run(fstab_cmd)
        # Create the entry to be added to /etc/fstab
        fstab_entry = f"UUID={UUID}    {mount_location_str}    ntfs    defaults,errors=remount-ro 0    1\n"

        # Open /etc/fstab in append mode and write the entry
        with open('/etc/fstab', 'a') as fstab_file:
            fstab_file.write(fstab_entry)

        print(f"{EXTERNAL_HD} mounted to boot succsessfully")
        print('/n')
        drive_mapping[EXTERNAL_HD] = {"UUID": UUID,
                                      "back_up_name": back_up_drive_name,
                                      "signal_pin" : signal_pin,
                                      "mount_location": mount_location_str}

    return drive_mapping
    


def hash_init(config_data):
    for index, object in enumerate(config_data['HD_map']):
        # get drive mapping details:
        EXTERNAL_HD = config_data["HD_map"][object]["name"]
        back_up_drive_name = hd_name = config_data["HD_map"][object]["back_up_name"]
        signal_pin= hd_name = config_data["HD_map"][object]["GPIO_pin"]

        SOURCE_DIR = os.getcwd()
        DESTINATION_DIR = f"/media/{EXTERNAL_HD}"


        #print("dst = ",DESTINATION_DIR)

        """
        locs = [select_random_location(SOURCE_DIR),
                 select_random_location(DESTINATION_DIR)]
        """
        locs = [select_random_location(SOURCE_DIR),
                 DESTINATION_DIR]

        hash_locations = create_hash_file(locs)

        with open(".env", "a", encoding="utf8") as f:
            f.write(f"{EXTERNAL_HD}_SRC_VALIDATION_HASH_LOC = '{hash_locations[0]}'\n")
            f.write(f"{EXTERNAL_HD}_DST_VALIDATION_HASH_LOC = '{hash_locations[1]}'")
        print("hash checks written")
