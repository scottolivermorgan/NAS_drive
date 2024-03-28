import subprocess

def sync_directories():
    source_dir = "/mnt/komga"
    destination_dir = "/media/HD_1/Media/metadata/"

    # Construct rsync command
    rsync_command = [
        "rsync",
        "-av",  # Options for archive mode and verbose output
        "--delete",  # Delete extraneous files from destination directories
        source_dir,
        destination_dir
    ]

    try:
        # Execute rsync command
        subprocess.run(rsync_command, check=True)
        print("Directories synced successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error syncing directories: {e}")



#TODO mkdir FIRST if dosent exist
# Function to restore Jellyfin data from external hard drive to local.
def restore_metadata():
    source_directory = "/media/HD_1/Media/metadata/komga"
    destination_directory = "/mnt/"

    # Construct the rsync command
    rsync_command = [
        "rsync",
        "-avz",  # Options: archive, verbose, compress
        source_directory,
        destination_directory
    ]

    try:
        # Execute the rsync command using subprocess
        subprocess.run(rsync_command, check=True)
        print("Directories synced successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error syncing directories: {e}")

#sync_directories()
#restore_metadata()