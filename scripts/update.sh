#!/bin/bash 

echo "Updating packages"
sudo apt-get update -y

echo "Upgrading packages"
sudo apt-get upgrade -y

echo "Updates complete, rebooting"
sudo reboot