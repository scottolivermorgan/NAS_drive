#!/bin/bash

# Add package to install security fixes every day.
echo "Installing unattended-upgrades"
apt install unattended-upgrades -y

# Add mail utils for update to root user.
echo "Installing mailutils"
apt install mailutils -y

# Instsll fail2ban
echo "Installing fail2ban"
apt install fail2ban -y

# Install firewall and allow required ports
echo "Installing firewall"
apt install ufw -y

# Allow apache access for anyone
echo "Adding allow rules for HTTP and HTTPS in firewall"
ufw allow 80
ufw allow 443

# Allow SSH
echo "Adding allow rule for modified SSH port in firewall"
ufw allow 1111

# Allow Plex
echo "Adding allow rules for default plex wall"
ufw allow 32400

# Enable firewall
echo "activating firewall"
sudo ufw enable

# Set root user to recive email updates of upgrades.
echo "Set root user to recive email updates of upgrades"
sed -i 's/^\/\/Unattended-Upgrade::Mail ""/Unattended-Upgrade::Mail "root";/' /etc/apt/apt.conf.d/50unattended-upgrades

# Set the periodic upgrade
echo "Setting periodic upgrades"
echo "APT::Periodic::Enable “1”;
APT::Periodic::Update-Package-Lists “1”;
APT::Periodic::Download-Upgradeable-Packages “1”;
APT::Periodic::Unattended-Upgrade “1”;
APT::Periodic::AutocleanInterval “1”;
APT::Periodic::Verbose “2”;" | sudo tee -a /etc/apt/apt.conf.d/02periodic

# Always require pasword for sudo
#sed -i 's/scott ALL=(ALL) NOPASSWD: ALL/scott ALL=(ALL) PASSWD: ALL/' /etc/sudoers.d/010_pi-nopasswd

# Change default port on SSH connection:
echo "Changing default SSH port"
sed -i 's/#Port 22/Port 1111/' /etc/ssh/sshd_config
service ssh restart