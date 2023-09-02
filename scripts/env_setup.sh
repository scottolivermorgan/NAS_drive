#!/bin/bash

# Retrive current user and set as environment variable
export UN=$(whoami)

# Prompt user for password
echo "Create nextcloud user: "
read nc_user

# Set the password as an environment variable
export NC_USER="$nc_user"

echo "Next cloud user name has been set as the environment variable NC_USER"

# Prompt user for password
echo "Set nextcloud user password: "
read nc_password

# Set the password as an environment variable
export NC_PASSWORD="$nc_password"

echo "Password has been set as the environment variable NC_PASSWORD"

echo "Enter name of external hard drive:"
read external_hd

export DRIVE_1_UUID=$(blkid | grep -rn 'LABEL="'$external_hd'"' | grep -o ' UUID="[^"]*' | awk -F= '{print $2}' | tr -d '"')