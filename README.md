TODO:
- script to prompt and set envvariables to set/keep consistant users, pw ect
eg: mv /home/pi/NAS_drive/scripts/nextcloud/nextcloud.conf /etc/apache2/sites-available/ in nextcloud-installation.sh
- update scripts to read env vars
- script to automate gui config on NC
- script to automate gui config on Plex.

## Initial Pi 4 Setup
Download SD card formating software:
https://www.sdcard.org/downloads/formatter/

Format card on local machine:
![formatSD](./assets/pi_setup/format_SD.PNG)

Download Raspberry Pi Imager:
https://www.raspberrypi.com/software/

Run Raspberry Pi Imager and flash OS,
Select settings (cog wheel - lower right)

![formatSD](./assets/pi_setup/imager_screen_1.PNG)

Select 'Enable shh'
Select 'Use password authentication'
'set authorised keys' auto fills to local user.
enter username and password.

![formatSD](./assets/pi_setup/imager_screen_2.PNG)

Select 'Configure wireless LAN option and enter network details.
![formatSD](./assets/pi_setup/imager_screen_3.PNG)

Local settings auto filled, if not complete.
![formatSD](./assets/pi_setup/imager_screen_4.PNG)

Set hotsname as Pi , enable SSH and select use password authentication.
![formatSD](./assets/pi_setup/pialt.PNG)

Save and write SD, takes a few minutes.
Insert SD and turn on pi, nav to router on local network (192.168.1.1 for me) and login to router,  navigate to connected devices and find Pi address.

## Nextcloud ##
On network connected computer open Powershell:
``ssh <username>@192.168.1.x -v``

Enter password set when flashing OS in steps above.

Clone this repo:
``git clone https://github.com/scottolivermorgan/NAS_drive.git``

Change into repo folder:
``cd NAS_drive/scripts``

Update packages and reboot Pi:
``sudo sh update.sh``

Restablish SSH connection (as above) after Pi rebooted & change into repo folder:
``cd NAS_drive/scripts/nextcloud``

Install nexcloud dependancies and follw prompts:
``sudo sh nextcloud-dependancies.sh``

Setup initial databse and user for nextcloud, follow prompts:
``sudo sh nextcloud-setup.sh``

Install nextcloud:
``sudo sh nextcloud-installation.sh``

Reboot after completeion
``sudo reboot``

# Enable external storage via gui

``lsblk``     - Check mount point is sda1

``sudo sh mount-drives.sh``

``sudo reboot``

## Add external storage via gui under /media/harddrive1

## Plex

``sudo sh update.sh``

``cd NAS_drive/scripts/plex``

``sudo sh plex-installation.sh``

Access Plex at 192.168.1.9:32400/web

Sign in/create account and addexternal lib via GUI
Add Libary > harddrive1

## Backup drive
Relay wiring:
__Relay__  __Pin__
__+__  =    __5v Power__ (board no# 2)
__-__  =     __Ground__   (board no# 14)
__s__  =    __GPIO 14__  (board no# 8)

![pinout](./assets/backup_setup/pi4_pinout.PNG)

Switch to correct dir:
``cd NAS_drive/scripts/backup_drive``

Schedule relay (_note_ runs in superuser cron jobs):
``sudo sh schedule-backup.sh``