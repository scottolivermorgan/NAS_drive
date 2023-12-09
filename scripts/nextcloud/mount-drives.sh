#!/bin/bash

# Look up UUID of eternal hd and set as an environment variable
# Note: Commands extract full details of drive from blkid,
# parse for uuid, strip 'uuid=', strip leading whitespace.
export DRIVE_1_UUID=$(blkid --match-token LABEL="$EXTERNAL_HD" | grep -o ' UUID="[^"]*' | sed 's/UUID="//' | sed 's/^ *//')

# Harddrive location
mkdir /media/hardrive1

# Mount harddrive on boot
echo "UUID=$DRIVE_1_UUID    /media/hardrive1               ntfs    defaults,errors=remount-ro 0       1" >> /etc/fstab

sudo -u www-data php /var/www/nextcloud/occ files:scan --all --verbose