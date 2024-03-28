import subprocess

# Function to sync local Jellyfin metadata to external hard drive.
def sync_directories():
    # Define source and destination directories
    directories = [
        ("/mnt/jellyfin/cache/", "/media/HD_1/Media/metadata/jellyfin/cache/"),
        ("/mnt/jellyfin/config/", "/media/HD_1/Media/metadata/jellyfin/config/")
    ]

    # Iterate over directories and perform rsync
    for src, dest in directories:
        rsync_command = [
            "rsync",
            "-avz",  # Options for rsync: archive mode, verbose, compress
            "--delete",  # Delete extraneous files from dest dirs
            src,
            dest
        ]
        try:
            subprocess.run(rsync_command, check=True)
            print(f"Synced {src} to {dest} successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error syncing {src} to {dest}: {e}")

sync_directories()
# Function to restore Jellyfin data from external hard drive to local.