import hashlib
from datetime import datetime
import random
import os
from dotenv import load_dotenv

def create_hash_file(paths: List[str]) -> List[str]:
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
