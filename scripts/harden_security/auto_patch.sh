# Add package to install security fixes every day.
echo "Installing unattended-upgrades"
apt install unattended-upgrades

# Add mail utils for update to root user.
apt install mailutils

# Set root user to recive email updates of upgrades.
sed -i 's/^\/\/Unattended-Upgrade::Mail ""/Unattended-Upgrade::Mail "root";/' /etc/apt/apt.conf.d/50unattended-upgrades

# Set the periodic upgrade
echo "APT::Periodic::Enable “1”;
APT::Periodic::Update-Package-Lists “1”;
APT::Periodic::Download-Upgradeable-Packages “1”;
APT::Periodic::Unattended-Upgrade “1”;
APT::Periodic::AutocleanInterval “1”;
APT::Periodic::Verbose “2”;" | sudo tee -a /etc/apt/apt.conf.d/02periodic