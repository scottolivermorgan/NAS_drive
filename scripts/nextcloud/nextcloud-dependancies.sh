#!/bin/bash

#remove unused packages and clean cache
echo "remove unused packages and cleaning cache"
yes | sudo apt autoremove
yes | sudo apt clean

# Install apache
# Server version: Apache/2.4.57 (Debian)
# Server built:   2023-04-13T03:26:51
echo "Installing apahe2"
yes | sudo apt install apache2

# Add third party PHP repo
echo " Adding third party PHP repos"
curl https://packages.sury.org/php/apt.gpg | sudo tee /usr/share/keyrings/suryphp-archive-keyring.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/suryphp-archive-keyring.gpg] https://packages.sury.org/php/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/sury-php.list
sudo apt update

# Install relevent PHP packages
echo "Installing required PHP packages"
yes | sudo apt-get install libapache2-mod-php8.2 php8.2-zip php8.2-mysql php8.2-curl php8.2-xml php8.2-mbstring php8.2-gd php8.2-smbclient php8.2-gmp php8.2-bcmath php8.2-intl php8.2-imagick

# Install mariaDB
# mariadb  Ver 15.1 Distrib 10.11.4-MariaDB, for debian-linux-gnu (aarch64) using  EditLine wrapper
echo "Installing MySQL"
yes | sudo apt install mariadb-server