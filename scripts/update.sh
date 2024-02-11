#!/bin/bash 

apt-get update 
apt-get upgrade
sudo python pip install -r requirements.txt
echo "apt update complete, rebooting"
sudo reboot