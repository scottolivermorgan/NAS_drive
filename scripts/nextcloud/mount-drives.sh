# Harddrive location
mkdir /media/harddrive1

# Mount harddrive on boot
#echo "/dev/sda2 /media/hardrive1    auto    uid=1000,gid=1000,noatime 0 0" >> /etc/fstab

echo "UUID=C41E05971E0583A0    /media/hardrive1               nfts    defaults,errors=remount-ro 0       1" >> /etc/fstab