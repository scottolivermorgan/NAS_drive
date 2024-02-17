#!/bin/bash 

echo "Updating packages"
apt-get update 

echo "Upgrading packages"
apt-get upgrade

echo "Installing Python Dependancies"
cd /home/$USER/NAS_drive       ########### BUG: running as root
sudo pip install -r requirements.txt

echo "Updates complete, rebooting"
sudo reboot