# Change to default Apache2 directory
cd /var/www

# Download Nextcloud
wget https://download.nextcloud.com/server/releases/latest.tar.bz2

# Extract the archive
tar -xvf latest.tar.bz2

# Make directory for Nextcloud to operate in
mkdir -p /var/www/nextcloud/data

# Update permissions
chown -R www-data:www-data /var/www/nextcloud/

#Move Nextcloud config file to correct location for Apache
mv /home/pi/NAS_drive/scripts/nextcloud/nextcloud.conf /etc/apache2/sites-available/

# Point Apahe2 to config file for Nextcloud
a2ensite nextcloud.conf

# Restart Apache2 to load new configuration
systemctl reload apache2