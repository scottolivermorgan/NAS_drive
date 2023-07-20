Format SD card
https://www.sdcard.org/downloads/formatter/

Flash Pi os with Raspberry Pi Imager
https://www.raspberrypi.com/software/

settings:
Enable shh -- on
    - defualt check - Use password authentication
Set username and password
    - Username <username>
    - Password <password>

Insert and turn on pi, nav to 192.168.1.1 and login to router, connected devices find Pi address.

Powershell
ssh <username>@192.168.1.x -v
- enter <password>

May need to update user/.shh if changes made easiest to just clear.

git clone https://github.com/scottolivermorgan/NAS_drive.git

cd NAS_drive

sudo sh update.sh

restablish ssh connection

cd NAS_drive

sudo sh nextcloud-dependancies.sh

sudo sh nextcloud-setup.sh

sudo sh nextcloud-installation.sh
