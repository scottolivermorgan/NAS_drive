#!/bin/bash

#remove unused packages and clean cache
echo "remove unused packages and cleaning cache"
sudo apt autoremove
sudo apt clean

# Install apache
echo "Installing apahe2"
apt install apache2

# Add third party PHP repo
echo " Adding third party PHP repos"
curl https://packages.sury.org/php/apt.gpg | sudo tee /usr/share/keyrings/suryphp-archive-keyring.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/suryphp-archive-keyring.gpg] https://packages.sury.org/php/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/sury-php.list
apt update

# Install relevent PHP packages
echo "Installing required PHP packages"
apt install php8.1 php8.1-gd php8.1-sqlite3 php8.1-curl php8.1-zip php8.1-xml php8.1-mbstring php8.1-mysql php8.1-bz2 php8.1-intl php8.1-smbclient php8.1-imap php8.1-gmp php8.1-bcmath libapache2-mod-php8.1

# Install mariaDB
echo "Installing MySQL"
apt install mariadb-server

echo "Nextcloud dependancies installed, please run nextcloud-setup"
