import subprocess
from library.helpers import get_files_created_today

if __name__ == "__main__":
    fp = ['/media/HD_1/Media/TV Shows', '/media/HD_1/Media/Movies']

    for folder in fp:
        updated, new_files = get_files_created_today(folder)

        if updated:
            # Create the message string with the list of new files
            new_files_message = 'New Media available: ' + ', '.join(new_files)

            # Prepare the command with the updated message
            command = ['curl', '-d', new_files_message, 'http://192.168.1.9:8090/media_updated']
            
            # Make the API call
            ntfy_call = subprocess.run(command, capture_output=True)
