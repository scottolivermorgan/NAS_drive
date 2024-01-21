#!/bin/bash

# Define the path to your config.json file
config_file="config.json"

# Check if the config file exists
if [ ! -f "$config_file" ]; then
    echo "Error: config.json not found."
    exit 1
fi

# Use jq to loop over the items in HD_map and print the "name" value
echo "$json" | jq '.HD_map | to_entries[] | .value.name'

# Parse the JSON and count the objects within "HD_map"
#available_drives=$(jq '.HD_map | length' "$config_file")
#
## Set the environment variable
#export AVALIBLE_DRIVES="$available_drives"
#
## Print the result
#echo "AVALIBLE_DRIVES is set to: $AVALIBLE_DRIVES"
#
## Loop over the drives
#for i in "$AVALIBLE_DRIVES"; do
#  echo "Processing drive: $$AVALIBLE_DRIVES"
#  # Add your logic here for each drive
#done
#echo "Enter current user name?"
#read User_name
#export UN="$User_name"
#
#echo "Install Next Cloud y/n?"
#read nc_option
#
#if [ "$nc_option" = "y" ]; then
#    echo "Create nextcloud user:"
#    read nc_user
#    export NC_USER="$nc_user"
#    echo "Set nextcloud user password: "
#    read nc_password
#    export NC_PASSWORD="$nc_password"
#fi
#
#echo "Attach external Hard drive? y/n?"
#read ext_hd
#
#if [ "$ext_hd" = "y" ]; then
#    echo "Enter name of external hard drive:"
#    read external_hd
#    export EXTERNAL_HD="$external_hd"
#fi
#
#echo "Configure air gapped backup y/n?"
#read ag_bu
#
#if [ "$ag_bu" = "y" ]; then
#    echo "somthing"
#fi
#
#echo "Configure shutdown switch y/n?"
#read shutdown_switch
#
#if [ "$shutdown_switch" = "y" ]; then
#    echo "shutdown_switch"
#fi
#
#echo "Install Plex server y/n?"
#read plex
#
#if [ "$plex" = "y" ]; then
#    echo "plex"
#fi
#
#if [ "$nc_option" = "y" ]; then
#    sh NAS_drive/scripts/nextcloud/nextcloud-dependancies.sh
#    sh NAS_drive/scripts/nextcloud/nextcloud-installation.sh
#    sh NAS_drive/scripts/nextcloud/nextcloud-setup.sh
#fi
#
#if [ "$ext_hd" = "y" ]; then
#    sh NAS_drive/scripts/nextcloud/mount-drives.sh
#    echo "enable external storage via nextcloud GUI, type y when enabled."
#    read dummy
#    #sudo -u www-data php /var/www/nextcloud/occ files:scan --all --verbose
#fi
#
#if [ "$ag_bu" = "y" ]; then
#    sh NAS_drive/scripts/backup_drive/schedule-backup.sh
#fi
#
#if [ "$ag_bu" = "y" ]; then
#    sh NAS_drive/scripts/shutdown_switch/shutdown.sh
#fi
#
#if [ "$plex" = "y" ]; then
#    sh NAS_drive/scripts/plex/plex-installation.sh
#    sh NAS_drive/scripts/plex/mv_meta_loc.sh
#fi
#
#yes | sudo sh NAS_drive/scripts/harden_security/auto_patch.sh
#
#sudo reboot