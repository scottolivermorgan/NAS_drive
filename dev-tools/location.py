import os
import random

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

# Input folder path
folder_name = input("Enter the folder name: ")

# Check if the folder exists
if not os.path.exists(folder_name):
    print(f"The folder '{folder_name}' does not exist.")
else:
    random_location = select_random_location(folder_name)
    if random_location:
        print(f"Random location within '{folder_name}':")
        print(random_location)