# Create & configure database for nextcloud

echo "CREATE DATABASE nextclouddb;
      CREATE USER 'nextclouduser'@'localhost' IDENTIFIED BY 'shieldsDown';
      GRANT ALL PRIVILEGES ON nextclouddb.* TO 'nextclouduser'@'localhost';
      FLUSH PRIVILEGES;
      Quit" | sudo mysql -u root -p
