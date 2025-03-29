#!/bin/bash

# Run rsync and capture both output and error messages
CMD_OUTPUT=$(sudo rsync -av /media/HD_1/ /media/BU_1/ 2>&1)

# Check if the rsync command was successful
if [ $? -eq 0 ]; then
    # If rsync is successful, send success status with verbose output
    curl -d "Backup Successful: $CMD_OUTPUT" http://192.168.1.9:8090/backup_status
else
    # If rsync failed, send failure status along with error output
    curl -d "Backup Failed: $CMD_OUTPUT" http://192.168.1.9:8090/backup_status
fi
