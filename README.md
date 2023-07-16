Format SD card
https://www.sdcard.org/downloads/formatter/

Flash Pi os with Raspberry Pi Imager
https://www.raspberrypi.com/software/

Insert and turn on pi, nav to 192.168.1.1 and login to router, connected devices find Pi address.

Powershell
ssh pi@192.168.1.x -v
enter password

May need to update user/.shh if changes made easiest to just clear.

git clone https://github.com/scottolivermorgan/NAS_drive.git

sudo sh update.sh

restablish ssh connection

sudo sh nextcloud-dependancies.sh

sudo sh nextcloud-setup.sh

sudo sh nextcloud-installation.sh



