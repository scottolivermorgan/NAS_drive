#!/bin/bash 

echo "Updating packages"
sudo apt-get update -y

echo "Upgrading packages"
sudo apt-get upgrade -y

echo "Installing Python Dependancies"
cd /home/$USER/NAS_drive       ########### BUG: running as root
sudo pip install -r requirements.txt

echo "Updates complete, rebooting"
sudo reboot