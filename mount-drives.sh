# Harddrive location
mkdir /media/harddrive1

# Mount harddrive on boot
echo "/dev/sda2 /media/hardrive1    auto    uid=1000,gid=1000,noatime 0 0" >> /etc/fstab