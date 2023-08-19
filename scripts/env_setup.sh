#!/bin/bash

# Retrive current user and set as environment variable
export UN=$(whoami)

# Prompt user for password
read -s -p "Create nextcloud user: " nc_user
echo

# Set the password as an environment variable
export NC_USER="$nc_user"

echo "Password has been set as the environment variable NC_USER"

# Prompt user for password
read -s -p "Set nextcloud user passwor: " nc_password
echo

# Set the password as an environment variable
export NC_PASSWORD="$nc_password"

echo "Password has been set as the environment variable NC_PASSWORD"
