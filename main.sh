#!/bin/bash

echo "Install Next Cloud y/n?"
read nc_option

if [ "$nc_option" = "y" ]; then
    echo "Create nextcloud user:"
    read nc_user
    export NC_USER="$nc_user"
    echo "Set nextcloud user password: "
    read nc_password
    export NC_PASSWORD="$nc_password"
fi

echo "Attach external Hard drive? y/n?"
read ext_hd

if [ "$ext_hd" = "y" ]; then
    echo "Enter name of external hard drive:"
    read external_hd
    export EXTERNAL_HD="$external_hd"
fi

echo "Configure air gapped backup y/n?"
read ag_bu

if [ "$ag_bu" = "y" ]; then
    echo "somthing"
fi

echo "Configure shutdown switch y/n?"
read shutdown_switch

if [ "$shutdown_switch" = "y" ]; then
    echo "shutdown_switch"
fi

echo "Install Plex server y/n?"
read plex

if [ "$plex" = "y" ]; then
    echo "plex"
fi

if [ "$nc_option" = "y" ]; then
    sh NAS_drive/scripts/nextcloud/nextcloud-dependancies.sh
    sh NAS_drive/scripts/nextcloud/nextcloud-installation.sh
    sh NAS_drive/scripts/nextcloud/nextcloud-setup.sh
fi