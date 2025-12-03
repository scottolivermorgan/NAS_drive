import os
import json
import datetime

def get_file_sizes(root_dir="/"):
    file_sizes = {}

    # Walk through the directory structure starting from root_dir
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip the /media and /proc directories
        if "/media" in dirpath or "/proc" in dirpath:
            continue

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            
            # Check if the file is a symbolic link
            if os.path.islink(file_path):
                # Get the real path and check if it's the same as the original path
                real_path = os.path.realpath(file_path)
                # Avoid circular links by checking if the real path is still within the original directory
                if real_path == file_path:
                    continue  # Skip if it points back to itself

            try:
                # Get the file size in bytes
                file_size = os.path.getsize(file_path)
                file_sizes[file_path] = file_size
            except FileNotFoundError:
                # In case the file has been deleted during traversal
                continue
            except PermissionError:
                # In case the program does not have permission to access a file
                print(f"Permission denied: {file_path}")
                continue
            except OSError as e:
                # Handle other possible OS errors, like the one you encountered
                print(f"OSError while accessing {file_path}: {e}")
                continue

    return file_sizes

def save_file_sizes_to_json(file_sizes):
    # Get the current datetime to use as the filename
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Define the JSON filename
    json_filename = f"file_sizes_{current_datetime}.json"

    # Write the file_sizes dictionary to the JSON file
    with open(json_filename, "w") as json_file:
        json.dump(file_sizes, json_file, indent=4)
    
    print(f"File sizes have been saved to {json_filename}")

# Example usage
file_sizes = get_file_sizes("/")
save_file_sizes_to_json(file_sizes)
