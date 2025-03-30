import hashlib
import subprocess
import RPi.GPIO as GPIO
from datetime import datetime
import random
import os
from dotenv import load_dotenv
import time
import yaml


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
        print("path = ", path)
        with open(file_name, "w") as file:
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


def pre_sync_hash_verification(config_data) -> bool:
    """
    Perform pre-synchronization hash verification between a source and destination hash.

    This function reads hash values from the source and destination files,
    adjusts the destination hash using the `hash_offset` function, and compares
    the result with the source hash.

    Returns:
        bool: True if the source hash matches the adjusted destination hash, False otherwise.
    """
    load_dotenv()
    checks = []
    for object in config_data["HD_map"]:
        # get drive mapping details:
        EXTERNAL_HD = config_data["HD_map"][object]["name"]
        # Set enviroment variables
        src = os.getenv(f"{EXTERNAL_HD}_SRC_VALIDATION_HASH_LOC")
        dst = os.getenv(f"{EXTERNAL_HD}_DST_VALIDATION_HASH_LOC")

        with open(src, "r", encoding="utf8") as f:
            src_hash = f.readlines()

        with open(dst, "r", encoding="utf8") as f:
            dst_hash = f.readlines()
            dst_hash = hash_offset(dst_hash[0], reset=True)

        if src_hash[0] == dst_hash:
            checks.append(True)
        else:
            checks.append(False)
    return checks


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
    offset = ""
    for i in hash_key:
        if reset:
            offset += chr(ord(i) - 1)
        else:
            offset += chr(ord(i) + 1)

    return offset


def mount_HD_from_config(config_data):
    """
    Mounts external hard drives (HD) based on the configuration data provided.

    Args:
        config_data (dict): A dictionary containing configuration data, including HD mapping details.

    Returns:
        dict: A dictionary mapping external HD names to their details, including backup name,
            signal pin, UUID, and mount location.

    Raises:
        OSError: If there are issues with subprocess calls or file operations.

    Note:
        This function assumes the availability of the 'blkid' command and relies on subprocess
        calls to interact with system utilities. It also requires sudo privileges for creating
        directories and modifying the fstab file.

    Example:
        Sample config_data:
        {
            'HD_map': {
                'hd1': {
                    'name': 'ExternalHD1',
                    'back_up_name': 'BackupHD1',
                    'GPIO_pin': 17
                },
                'hd2': {
                    'name': 'ExternalHD2',
                    'back_up_name': 'BackupHD2',
                    'GPIO_pin': 18
                }
            }
        }

        Example usage:
        >>> config_data = {...}  # Provide appropriate configuration data
        >>> mappings = mount_HD_from_config(config_data)
        >>> print(mappings)
        {'ExternalHD1': {'back_up_name': 'BackupHD1', 'signal_pin': 17, 'UUID': '...', 'mount_loc': '...'},
         'ExternalHD2': {'back_up_name': 'BackupHD2', 'signal_pin': 18, 'UUID': '...', 'mount_loc': '...'}}

    """

    drive_mapping = {}

    for object in config_data["HD_map"]:
        # get drive mapping details:
        EXTERNAL_HD = config_data["HD_map"][object]["name"]
        print(f"Found {EXTERNAL_HD}")
        back_up_drive_name = config_data["HD_map"][object]["back_up_name"]
        signal_pin = config_data["HD_map"][object]["GPIO_pin"]

        # Build shell cmd's to pass to subprocesses:
        # Look up UUID of eternal hd and set as an environment variable
        # Note: Commands extract full details of drive from blkid,
        # parse for uuid, strip 'uuid=', strip leading whitespace.
        UUID_cmd = f"blkid --match-token \"LABEL={EXTERNAL_HD}\" | grep -o ' UUID=\"[^\"]*\"' | sed 's/UUID=\"//' | sed 's/^ *//'"
        UUID = subprocess.run(UUID_cmd, shell=True, capture_output=True, text=True)

        # If UUID found, format and add to fstab file to boot
        if UUID.returncode == 0:
            # Format str:
            output_string = UUID.stdout.strip().replace('"', "")

            # Get HD format type
            HD_type_cmd = f"blkid | grep 'LABEL=\"{EXTERNAL_HD}\"' | awk -F 'TYPE=' '{{print $2}}' | awk -F '\"' '{{print $2}}'"
            HD_type = subprocess.run(
                HD_type_cmd, shell=True, capture_output=True, text=True
            )

            # Get format type
            type_output = HD_type.stdout.strip()
            print(type_output)

            # User feed back:
            print(f"UUID found: {output_string}, of type: {type_output}")
            print("Making file mount")

            # Make dir to mount drive:
            mount_location_str = f"/media/{EXTERNAL_HD}"
            subprocess.run(["sudo", "mkdir", f"/media/{back_up_drive_name}"])
            MOUNT_DIR = subprocess.run(["sudo", "mkdir", mount_location_str])
            print("Mount point created, updating fstab")

            # Edit fstab to mount drive on boot:
            fstab_entry = f"UUID={output_string}    {mount_location_str}    {type_output}    defaults,errors=remount-ro 0    1\n"
            with open("/etc/fstab", "a") as f:
                f.write(fstab_entry)

            # Update dict with HD details:
            drive_mapping[EXTERNAL_HD] = {
                "back_up_name": back_up_drive_name,
                "signal_pin": signal_pin,
                "UUID": UUID,
                "mount_loc": MOUNT_DIR,
            }

        else:
            print("Failed to retrieve UUID.")

    # mount drives added to fstab
    print("Mounting new extenal hard drives")
    mount_drives = subprocess.run(["sudo", "mount", "-a"])
    dameon_reload = subprocess.run(["sudo", "systemctl", "daemon-reload"])

    return drive_mapping


def hash_init(config_data):
    """
    Initializes hash values for source and destination directories of external hard drives.

    Args:
        config_data (dict): A dictionary containing configuration data.
            It should have a key 'HD_map' containing information about external hard drives.

    Returns:
        None

    Raises:
        KeyError: If 'HD_map' key is missing in config_data or if required keys are not found within 'HD_map' entries.

    Note:
        This function assumes the structure of the 'config_data' dictionary to have the following keys:
        - 'HD_map': A dictionary where keys are identifiers for each external hard drive and values are dictionaries containing:
            - 'name': Name of the external hard drive.
            - 'back_up_name': Backup name of the external hard drive.
            - 'GPIO_pin': GPIO pin of the external hard drive.
    """
    for index, object in enumerate(config_data["HD_map"]):
        # get drive mapping details:
        EXTERNAL_HD = config_data["HD_map"][object]["name"]

        SOURCE_DIR = os.getcwd()
        DESTINATION_DIR = f"/media/{EXTERNAL_HD}"

        locs = [select_random_location(SOURCE_DIR), DESTINATION_DIR]
        print(f"Creating hash files in {locs}")

        hash_locations = create_hash_file(locs)

        with open(".env", "a", encoding="utf8") as f:
            f.write(f"{EXTERNAL_HD}_SRC_VALIDATION_HASH_LOC = '{hash_locations[0]}'\n")
            f.write(f"{EXTERNAL_HD}_DST_VALIDATION_HASH_LOC = '{hash_locations[1]}'")
        print("hash checks written")


def backup_HD(config_data):
    """
    Backs up data from specified external hard drives to designated backup drives.

    Args:
        config_data (dict): A dictionary containing configuration data for hard drive mapping.

    Returns:
        None

    Raises:
        Any exceptions raised during subprocess execution.

    Note:
        This function assumes the presence of a `power_on` function for controlling GPIO pins,
        and requires the `time`, `os`, and `subprocess` modules to be imported.

    Example:
        config_data = {
            'HD_map': {
                'drive1': {
                    'name': 'External_HD1',
                    'back_up_name': 'Backup_HD1',
                    'GPIO_pin': 18
                },
                'drive2': {
                    'name': 'External_HD2',
                    'back_up_name': 'Backup_HD2',
                    'GPIO_pin': 19
                }
            }
        }
        backup_HD(config_data)
    """

    print("Closing airgap")
    #TODO reinstate and write perm env vars (think failing after pi reboot)
    #checks = pre_sync_hash_verification(config_data)
    checks =[]

    if False in checks:
        print("Verification failed")
        command = ['curl', '-d', 'Hashchecks failed, backup failed', 'http://192.168.1.9:8090/backup_status']
        ntfy_call = subprocess.run(command, capture_output=True)
        return 1
    else:
        for object in config_data["HD_map"]:
            print("Verification sucsessfull")
            # get drive mapping details:
            EXTERNAL_HD = config_data["HD_map"][object]["name"]
            back_up_drive_name = hd_name = config_data["HD_map"][object]["back_up_name"]
            signal_pin = hd_name = config_data["HD_map"][object]["GPIO_pin"]

            print(f"Mounting {back_up_drive_name} hard drive")
            power_on(signal_pin, ON=True)
            time.sleep(20)
            mount_cmd = (
                f"lsblk -o LABEL,UUID | grep {back_up_drive_name} | awk '{{print $2}}'"
            )
            BU_UUID = subprocess.run(
                mount_cmd, shell=True, capture_output=True, text=True
            )
            output_string = BU_UUID.stdout.strip().replace('"', "")
            print(f"UUID found: {output_string}")

            mount_drive = subprocess.run(
                ["sudo", "mount", "-U", output_string, f"/media/{back_up_drive_name}"]
            )
            print(f"Syncing {back_up_drive_name} drive with {EXTERNAL_HD}")

            log_file_path = f"/home/{os.getenv('USER')}/NAS_drive/logs/sync_log.log"
            rsync_cmd = f"sudo rsync -av --log-file='{log_file_path}' /media/{EXTERNAL_HD}/* /media/{back_up_drive_name}"
            print(rsync_cmd)

            # Open log file in append mode so that logs get appended
            with open(log_file_path, "a") as log_file:
                sync = subprocess.run(
                    rsync_cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                if sync.returncode != 0:
                    command = ['curl', '-d', 'rsync backup failed', 'http://192.168.1.9:8090/backup_status']
                    ntfy_call = subprocess.run(command, capture_output=True)
                else:
                    command = ['curl', '-d', 'Backup Succsesfull', 'http://192.168.1.9:8090/backup_status']
                    ntfy_call = subprocess.run(command, capture_output=True)
                # Write stdout and stderr to both console and log file
                print(sync.stdout)
                print(sync.stderr)
                log_file.write(sync.stdout)
                log_file.write(sync.stderr)

            time.sleep(20)
            print(f"Unmounting drive: {back_up_drive_name}")
            unmount_drive = subprocess.run(
                ["sudo", "umount", f"/media/{back_up_drive_name}"]
            )

            print("Closing airgap")
            power_on(signal_pin, ON=False)


def get_files_created_today(directory):
    # List of media file extensions
    media_extensions = ['.mp4', '.mp3', '.wav', '.avi', '.mov', '.mkv']

    # Get today's date
    today = datetime.today().date()

    # List to hold the filenames of files created today that are media files
    files_created_today = []

    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Get the file path
            file_path = os.path.join(root, file)
            
            # Check if the file has a media extension
            if any(file.lower().endswith(ext) for ext in media_extensions):
                # Get the creation time of the file (in seconds)
                creation_time = os.path.getctime(file_path)
                
                # Convert creation time to a datetime object
                file_creation_date = datetime.fromtimestamp(creation_time).date()

                # Compare the file creation date with today's date
                if file_creation_date == today:
                    files_created_today.append(file_path)

    # If there are no media files created today, return False
    if not files_created_today:
        print("No new files created")
        return False, files_created_today
    else:
        return True, files_created_today
    

def activate_logical_volume(volume_group, logical_volume):
    """
    Activates the logical volume.
    """
    try:
        # Command to activate the logical volume
        command = ['sudo', 'lvchange', '-ay', f'{volume_group}/{logical_volume}']
        subprocess.run(command, check=True)
        print(f"Logical volume {logical_volume} activated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error activating logical volume {logical_volume}: {e}")
        

#def mount_logical_volume(mount_point, volume_group, logical_volume):
#    """
#    Mounts the logical volume to the specified mount point.
#    """
#    try:
#        # Command to mount the logical volume
#        command = ['sudo', 'mount', f'/dev/{volume_group}/{logical_volume}', mount_point]
#        subprocess.run(command, check=True)
#        print(f"Logical volume {logical_volume} mounted at {mount_point}.")
#    except subprocess.CalledProcessError as e:
#        print(f"Error mounting logical volume {logical_volume}: {e}")

def mount_logical_volume(mount_point, volume_group, logical_volume):
    """
    Mounts the logical volume to the specified mount point if it is not already mounted.
    """
    try:
        # Check if the logical volume is already mounted
        result = subprocess.run(['mount'], capture_output=True, text=True)
        if f'/dev/{volume_group}/{logical_volume}' in result.stdout:
            print(f"Logical volume {logical_volume} is already mounted at {mount_point}.")
        else:
            # Command to mount the logical volume
            command = ['sudo', 'mount', f'/dev/{volume_group}/{logical_volume}', mount_point]
            subprocess.run(command, check=True)
            print(f"Logical volume {logical_volume} mounted at {mount_point}.")
    except subprocess.CalledProcessError as e:
        print(f"Error mounting logical volume {logical_volume}: {e}")



def load_config_file(file_path):
    """
    Load a YAML config file and return the parsed data as a Python dictionary.
    
    :param file_path: The path to the YAML file to load.
    :return: A dictionary representing the YAML file's contents.
    """
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


#def execute_rsync():
#    """
#    Executes the rsync command to copy data from /media/HD_1/ to /media/BU_1/.
#    """
#    try:
#        # Command to execute rsync
#        command = ['sudo', 'rsync', '-av', '/media/HD_1/', '/media/BU_1/']
#        subprocess.run(command, check=True)
#        print("Rsync completed successfully.")
#        command = ['curl', '-d', 'Backup Succsesfull', 'http://192.168.1.9:8090/backup_status']
#        ntfy_call = subprocess.run(command, capture_output=True)
#
#    except subprocess.CalledProcessError as e:
#        print(f"Error executing rsync: {e}")
#        command = ['curl', '-d', 'Backup Succsesfull', 'http://192.168.1.9:8090/backup_status']
#        ntfy_call = subprocess.run(command, capture_output=True)

def execute_rsync():
    """
    Executes the rsync command to copy data from /media/HD_1/ to /media/BU_1/.
    """
    try:
        # Command to execute rsync
        command = ['sudo', 'rsync', '-av', '/media/HD_1/', '/media/BU_1/']
        
        # Capture the verbose output of the rsync command
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        
        # Get the verbose output from the rsync command
        rsync_output = result.stdout
        
        print("Rsync completed successfully.")
        
        # Send rsync output as part of the curl request
        curl_command = ['curl', '-d', f'Backup Successful: {rsync_output}', 'http://192.168.1.9:8090/backup_status']
        subprocess.run(curl_command, capture_output=True)

    except subprocess.CalledProcessError as e:
        print(f"Error executing rsync: {e}")
        
        # If rsync fails, capture the error message and send it via curl
        error_message = f"Backup Unsuccessful: {e.stderr if e.stderr else 'No error details'}"
        curl_command = ['curl', '-d', error_message, 'http://192.168.1.9:8090/backup_status']
        subprocess.run(curl_command, capture_output=True)