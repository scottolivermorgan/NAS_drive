#!/bin/bash 
sudo apt autoremove
sudo apt clean
apt install apache2
curl https://packages.sury.org/php/apt.gpg | sudo tee /usr/share/keyrings/suryphp-archive-keyring.gpg >/dev/null

echo "deb [signed-by=/usr/share/keyrings/suryphp-archive-keyring.gpg] https://packages.sury.org/php/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/sury-php.list
apt update

apt install php8.1 php8.1-gd php8.1-sqlite3 php8.1-curl php8.1-zip php8.1-xml php8.1-mbstring php8.1-mysql php8.1-bz2 php8.1-intl php8.1-smbclient php8.1-imap php8.1-gmp php8.1-bcmath libapache2-mod-php8.1