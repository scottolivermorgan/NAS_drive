#!/bin/bash

# Create & configure database for nextcloud
 echo "CREATE DATABASE nextclouddb;
      CREATE USER '$NC_USER'@'localhost' IDENTIFIED BY '$NC_PASSWORD';
      GRANT ALL PRIVILEGES ON nextclouddb.* TO '$NC_USER'@'localhost';
      FLUSH PRIVILEGES;
      Quit" | sudo mysql -u root -p

echo "Nextcloud-setup complete, please run nextcloud-installation"
