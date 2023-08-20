# Add package to install security fixes every day.
echo "Installing unattended-upgrades"
apt install unattended-upgrades

# Add mail utils for update to root user.
apt install mailutils

sed -i 's///Unattended-Upgrade::Mail "";/Unattended-Upgrade::Mail "root";/' /etc/apt/apt.conf.d/50unattended-upgrades