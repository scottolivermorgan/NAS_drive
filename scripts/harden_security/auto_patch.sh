# Add package to install security fixes every day.
echo "Installing unattended-upgrades"
apt install unattended-upgrades

# Add mail utils for update to root user.
apt install mailutils

# Instsll fail2ban
apt install fail2ban

# Install firewall and allow required ports
apt install ufw

# Allow apache access for anyone
ufw allow 80
ufw allow 443

# Allow SSH
ufw allow 1111

# Allow Plex
ufw allow 32400

# Enable firewall
sudo ufw enable

# Set root user to recive email updates of upgrades.
sed -i 's/^\/\/Unattended-Upgrade::Mail ""/Unattended-Upgrade::Mail "root";/' /etc/apt/apt.conf.d/50unattended-upgrades

# Set the periodic upgrade
echo "APT::Periodic::Enable “1”;
APT::Periodic::Update-Package-Lists “1”;
APT::Periodic::Download-Upgradeable-Packages “1”;
APT::Periodic::Unattended-Upgrade “1”;
APT::Periodic::AutocleanInterval “1”;
APT::Periodic::Verbose “2”;" | sudo tee -a /etc/apt/apt.conf.d/02periodic

# Always require pasword for sudo
#sed -i 's/scott ALL=(ALL) NOPASSWD: ALL/scott ALL=(ALL) PASSWD: ALL/' /etc/sudoers.d/010_pi-nopasswd

# Change default port on SSH connection:
sed -i 's/#Port 22/Port 1111/' /etc/ssh/sshd_config
service ssh restart