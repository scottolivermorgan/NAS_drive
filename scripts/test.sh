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


#remove unused packages and clean cache
echo "remove unused packages and cleaning cache"
sudo apt autoremove
sudo apt clean

# Install apache
echo "Installing apahe2"
yes | apt install apache2

# Add third party PHP repo
echo " Adding third party PHP repos"
curl https://packages.sury.org/php/apt.gpg | sudo tee /usr/share/keyrings/suryphp-archive-keyring.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/suryphp-archive-keyring.gpg] https://packages.sury.org/php/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/sury-php.list
apt update

# Install relevent PHP packages
echo "Installing required PHP packages"
yes | apt install php8.1 php8.1-gd php8.1-sqlite3 php8.1-curl php8.1-zip php8.1-xml php8.1-mbstring php8.1-mysql php8.1-bz2 php8.1-intl php8.1-smbclient php8.1-imap php8.1-gmp php8.1-bcmath libapache2-mod-php8.1

# Install mariaDB
echo "Installing MySQL"
yes | apt install mariadb-server

echo "Nextcloud dependancies installed, please run nextcloud-setup"


# Create & configure database for nextcloud

echo "CREATE DATABASE nextclouddb;
      CREATE USER '$NC_USER'@'localhost' IDENTIFIED BY '$NC_PASSWORD';
      GRANT ALL PRIVILEGES ON nextclouddb.* TO '$NC_USER'@'localhost';
      FLUSH PRIVILEGES;
      Quit" | sudo mysql -u root -p

echo "Nextcloud-setup complete, please run nextcloud-installation"

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
#error here on UN
mv /home/$UN/NAS_drive/scripts/nextcloud/nextcloud.conf /etc/apache2/sites-available/

# Point Apahe2 to config file for Nextcloud
a2ensite nextcloud.conf

# Restart Apache2 to load new configuration
systemctl reload apache2

# Harddrive location
mkdir /media/hardrive1

# Mount harddrive on boot
#echo "/dev/sda2 /media/hardrive1    auto    uid=1000,gid=1000,noatime 0 0" >> /etc/fstab

echo "UUID='$DRIVE_1_UUID'    /media/hardrive1               nfts    defaults,errors=remount-ro 0       1" >> /etc/fstab