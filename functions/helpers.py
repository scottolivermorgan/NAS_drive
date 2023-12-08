from dotenv import load_dotenv
import hashlib
from datetime import datetime
import random
import os

def create_hash_file(paths):
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
    # Create a list to store all file paths within the folder and its subfolders
    all_files = []

    # Walk through the folder and its subfolders to collect file paths
    # Only logs last dir if a file present in dir
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root)
            all_files.append(file_path)

    # Select a random file path
    random_location = random.choice(all_files)
    return random_location

def pre_sync_hash_verification():
    # Set enviroment variables
    load_dotenv()
    src = os.getenv("SRC_VALIDATION_HASH_LOC")
    dst = os.getenv("DST_VALIDATION_HASH_LOC")

    with open(src, 'r') as f:
        src_hash = f.readlines()
    
    with open(dst, 'r') as f:
        dst_hash = f.readlines()
        dst_hash = hash_offset(dst_hash[0], reset=True)
    
    if src_hash[0] == dst_hash:
        return True
    else:
        return False
    
def hash_offset(hash, reset):
    offset = ''
    for i in hash:
        if reset:
            offset += (chr(ord(i)-1))
        else:
            offset += (chr(ord(i)+1))

    return offset
