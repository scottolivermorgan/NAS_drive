#!/bin/bash

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "jq is not installed. Please install jq first."
    exit 1
fi

# Read and parse the JSON file
json_data=$(cat config.json)

# Loop through the "HD_map" entries and extract the "name" values
count=1
for hd_entry in $(echo "$json_data" | jq -r '.HD_map | keys[]'); do
    EXTERNAL_HD=$(echo "$json_data" | jq -r ".HD_map.$hd_entry.name")
    echo "Mounting : $EXTERNAL_HD"

    # Look up UUID of eternal hd
    # Note: Commands extract full details of drive from blkid,
    # parse for uuid, strip 'uuid=', strip leading whitespace.
    DRIVE_UUID=$(blkid --match-token LABEL="$EXTERNAL_HD" | grep -o ' UUID="[^"]*' | sed 's/UUID="//' | sed 's/^ *//')
    
    # Harddrive location
    mkdir /media/hardrive1
    
    # Mount harddrive on boot
    echo "UUID=$DRIVE_UUID    /media/hardrive1               ntfs    defaults,errors=remount-ro 0       1" >> /etc/fstab

    ((count++))

done