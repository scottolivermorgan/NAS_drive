#!/bin/bash 

echo "Updating packages"
apt-get update 

echo "Upgrading packages"
apt-get upgrade

echo "Installing Python Dependancies"
sudo python pip install -r requirements.txt

echo "Updates complete, rebooting"
sudo reboot