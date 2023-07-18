#!/bin/bash

#remove unused packages and clean cache
sudo apt autoremove -y
sudo apt clean -y

# Install apache
apt install apache2 -y

# Add third party PHP repo
curl https://packages.sury.org/php/apt.gpg | sudo tee /usr/share/keyrings/suryphp-archive-keyring.gpg >/dev/null -y
echo "deb [signed-by=/usr/share/keyrings/suryphp-archive-keyring.gpg] https://packages.sury.org/php/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/sury-php.list -y
apt update -y

# Install relevent PHP packages
apt install php8.1 php8.1-gd php8.1-sqlite3 php8.1-curl php8.1-zip php8.1-xml php8.1-mbstring php8.1-mysql php8.1-bz2 php8.1-intl php8.1-smbclient php8.1-imap php8.1-gmp php8.1-bcmath libapache2-mod-php8.1 -y

# Install mariaDB
apt install mariadb-server -y

# Create & configure database for nextcloud

echo "CREATE DATABASE nextclouddb;
      CREATE USER 'nextclouduser'@'localhost' IDENTIFIED BY 'shieldsDown';
      GRANT ALL PRIVILEGES ON nextclouddb.* TO 'nextclouduser'@'localhost';
      FLUSH PRIVILEGES;
      Quit" | sudo mysql -u root -p

# Change to default Apache2 directory
cd /var/www

# Download Nextcloud
wget https://download.nextcloud.com/server/releases/latest.tar.bz2

# Extract the archive
tar -xvf latest.tar.bz2

# Make directory for Nextcloud to operate in
mkdir -p /var/www/nextcloud/data

# Update permissions
chown -R www-data:www-data /var/www/nextcloud/

#Move Nextcloud config file to correct location for Apache
mv /home/pi/NAS_drive/nextcloud.conf /etc/apache2/sites-available/

# Point Apahe2 to config file for Nextcloud
a2ensite nextcloud.conf

# Restart Apache2 to load nextcloud confi
systemctl reload apache2