## Initial Pi 4 Setup

![formatSD](./assets/format_SD.PNG)

Format SD card
https://www.sdcard.org/downloads/formatter/

Flash Pi os with Raspberry Pi Imager
https://www.raspberrypi.com/software/

Settings:
Enable shh -- on
    - defualt check - Use password authentication
Set username and password
    - Username <username>
    - Password <password>

Insert SD and turn on pi, nav to 192.168.1.1 and login to router, connected devices find Pi address.

## Nextcloud 

Powershell
``ssh <username>@192.168.1.x -v``
- enter password

May need to update user/.shh if changes made easiest to just clear.

``git clone https://github.com/scottolivermorgan/NAS_drive.git``

``cd NAS_drive``

``sudo sh update.sh``

Restablish ssh connection after Pi rebooted.

``cd NAS_drive``

``sudo sh nextcloud-dependancies.sh``

``sudo sh nextcloud-setup.sh``

``sudo sh nextcloud-installation.sh``

``sudo reboot``

# Enable external storage via gui

``lsblk``     - Check mount point is sda1

``sudo sh mount-drives.sh``

``sudo reboot``

# Add external storage via gui under /media/harddrive1

## Plex

``sudo sh update.sh``

``sudo sh plex-installation.sh``

Access Plex at 192.168.1.100:32400/web

Sign in/create account and addexternal lib via GUI
Add Libary > harddrive1
