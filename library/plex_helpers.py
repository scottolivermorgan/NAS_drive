import os
import shutil


def organize_movie_files_into_dirs(input_path):
    """Organizes files in the specified directory by creating a directory for each file
    and moving the file into that directory.

    Args:
        input_path (str): The path to the directory containing files to be organized.

    Returns:
        None: This function does not return anything. It organizes files within the specified directory.

    Raises:
        None

    Example:
        Consider a directory named 'files' containing the following files:
            - file1.txt
            - file2.jpg
            - file3.py
        Calling organize_files('files') will create three directories within 'files':
            - file1 (containing file1.txt)
            - file2 (containing file2.jpg)
            - file3 (containing file3.py)
        The original files will be moved into their respective directories.
    """
    # Check if the input path exists
    if not os.path.exists(input_path):
        print("The specified path does not exist.")
        return

    # Scan the input path
    for item in os.listdir(input_path):
        item_path = os.path.join(input_path, item)

        # Check if it's a file
        if os.path.isfile(item_path):
            # Create a directory with the same name as the file
            directory_name = os.path.splitext(item)[0]
            directory_path = os.path.join(input_path, directory_name)

            # Check if the directory already exists
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

            # Move the file into the directory
            shutil.move(item_path, os.path.join(directory_path, item))


if __name__ == "__main__":
    org_files = input("Put movie files in their own directories y/n?")
    if org_files == "y":
        input_path = input("Enter directory, e.g.: /movies ")
        try:
            organize_movie_files_into_dirs(input_path)
        except:
            print("Invalid path")
