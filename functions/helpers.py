import hashlib
from datetime import datetime

def create_hash_file():
    # Get the current datetime
    current_datetime = datetime.now()

    # Convert the datetime to a string
    datetime_str = str(current_datetime)

    # Calculate the hash of the datetime string using SHA-256
    hash_object = hashlib.sha256(datetime_str.encode())
    hash_hex = hash_object.hexdigest()

    # Create a text file and write the hash to it
    file_name = f"hash_{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    with open(file_name, 'w') as file:
        file.write(hash_hex)

    print(f"Hash saved to {file_name}")

    return file_name

def select_random_location(folder_path):
    # Create a list to store all file paths within the folder and its subfolders
    all_files = []

    # Walk through the folder and its subfolders to collect file paths
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)

    # Check if any files were found
    if not all_files:
        print("No files found in the specified folder and its subfolders.")
        return None

    # Select a random file path
    random_location = random.choice(all_files)
    return random_location