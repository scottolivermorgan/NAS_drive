#!/bin/bash

# Change to default Apache2 directory
echo "Changing directory"
cd /var/www

# Download Nextcloud
echo "Downloading Nextcloud"
wget https://download.nextcloud.com/server/releases/nextcloud-27.0.1.tar.bz2

# Extract the archive
echo "Extracting Nextcloud"
sudo tar -xvf nextcloud-27.0.1.tar.bz2

# Make directory for Nextcloud to operate in
echo "Making Nextcloud Data Directory"
sudo mkdir -p /var/www/nextcloud/data

# Update permissions
echo " Updating permissions"
sudo chown -R www-data:www-data /var/www/nextcloud/

#Move Nextcloud config file to correct location for Apache
echo "Configuring apache for Nextcloud"
sudo mv /home/$UN/NAS_drive/scripts/nextcloud/nextcloud.conf /etc/apache2/sites-available/

# Point Apahe2 to config file for Nextcloud
sudo a2ensite nextcloud.conf

# Restart Apache2 to load new configuration
echo "Restaring Apache server"
sudo systemctl reload apache2