TODO:
- script to automate gui config on NC
- script to automate gui config on Plex.
- mount HD's via USID not path

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
enter username and password. __DO NOT USE DEFAULT USERNAME & PASSWORDS__.

![formatSD](./assets/pi_setup/imager_screen_2.PNG)

Select 'Configure wireless LAN option and enter network details.
![formatSD](./assets/pi_setup/imager_screen_3.PNG)

Local settings auto filled, if not complete.
![formatSD](./assets/pi_setup/imager_screen_4.PNG)

Set hotsname as Pi , enable SSH and select use password authentication.
![formatSD](./assets/pi_setup/pialt.PNG)

Save and write SD, takes a few minutes.
Insert SD and turn on pi, nav to router on local network (192.168.1.1 for me) and login to router,  navigate to connected devices and find Pi address.

# Enter Enviroment variables
On network connected computer open Powershell:
``ssh <username>@192.168.1.x -v``

Clone this repo:
``git clone https://github.com/scottolivermorgan/NAS_drive.git``

change dir
``cd NAS_drive/scripts``

run
``sudo sh env_setup.sh``
and enter prompts

TODO: retrive UUID of external HD and set here

# Update Pi
On network connected computer open Powershell:
``ssh <username>@192.168.1.x -v``

``yes | sudo sh env_setup.sh``
Follows prompts the set usernames and passwords.

# Nextcloud 
On network connected computer open Powershell:
``ssh <username>@192.168.1.x -v``

Change into repo folder:
``cd NAS_drive/scripts/nextcloud``

Install nexcloud dependancies and follw prompts:
``yes | sudo sh nextcloud-dependancies.sh``

Setup initial databse and user for nextcloud, follow prompts:
``sudo sh nextcloud-setup.sh``

Install nextcloud:
``yes | sudo sh nextcloud-installation.sh``

Reboot after completeion
``sudo reboot``

# Enable External Storage via GUI

``lsblk``     - Check mount point is sda1

``sudo sh mount-drives.sh``

Click top right userprofile icon and select Apps.
![addExt1](./assets/nextcloud_add_external_drive/nc1.PNG)

Scroll list and select Enable on External Storage support
![addExt1](./assets/nextcloud_add_external_drive/nc2.PNG)

Wait several seconds, again select user icon at top right and select Administrator settings.
![addExt1](./assets/nextcloud_add_external_drive/nc3.PNG)

Select External storage tab on left and add name, Local, and add mount point defined in mount-drives.sh - /media/harddrive1
![addExt1](./assets/nextcloud_add_external_drive/nc4.PNG)

Return to SSH shell and reboot Pi.
``sudo reboot``

## Plex
From SSH shell update packages if havent recently

``sudo sh update.sh``

Change directory to plex installation script
``cd NAS_drive/scripts/plex``

install plex
``sudo sh plex-installation.sh``

Access Plex at 192.168.1.x:32400/web -x dependant on your local network.

Sign in/create account and addexternal lib via GUI
Add Libary > harddrive1 (in this case as has been set in previouse steps)

## Backup drive
Relay wiring:

_note_ GPIOs 0-8, 14 & 15 appearhigh at boot, if connected to these pins relay will power up, connect 2nd HD then power down so don't use these pins.
__Relay__  __Pin__
__+__  =    __5v Power__ (board no# 2)
__-__  =     __Ground__   (board no# 14)
__s__  =    __GPIO 14__  (board no# 8)

![pinout](./assets/backup_setup/pi4_pinout.PNG)

Switch to correct dir:
``cd NAS_drive/scripts/backup_drive``

Schedule relay (_note_ runs in superuser cron jobs):
``sudo sh schedule-backup.sh``

## Add Powerdown Button
Pi dosen't ship with power off button, shutting down cleanly avoids SD card corruption so add a switch and python script to enable clean shutdowns before turing off at plug.

Use board pins __39__ (ground) and __40__ (GPIO21):
![pinout](./assets/shutdown_switch/shutdown_switch_pinout.PNG)

Change working directory
``cd /NAS_drive/scripts/shutdown_switch``

Edit start up scripts to run shutdown.py to listen to button
``sudo sh shutdown.sh``

Reboot Pi
``sudo reboot``

## Harden Security
Change working dir
`` cd NAS_drive/scripts/harden_security``

Install packages to auto update security patchs
``sudo sh auto_patch.sh``
_Note:_ SSH port changed from 22 to 1111

Check for users with empty passwords
``sudo awk -F: '($2 == "") {print}' /etc/shadow``

Lock any applicable accounts
``passwd -l <username>``

Check expected logins
``lslogins -u``

Check any unexpected services running
``sudo service --status-all``

Check SHH root login disabled
``sudo nano /etc/ssh/sshd_config``

Verify following exists
``#PermitRootLogin prohibit-password``

## External Access
Resources:
https://help.nextcloud.com/t/how-to-access-from-outside-your-network/126311
https://techmadeeasy.co.uk/2020/03/access-a-nextcloud-server-from-outside-your-home-network/
Nextcloud desktop client:
https://nextcloud.com/install/#install-clients

Set up account and domain name with following DDNS service:
https://www.noip.com/

Open SSH to Pi andchange dir to
``cd /var/www/html/nextcloud/config``

Open config file
``sudo nanoconfig.php``

add domain name to
``'trusted_domains' =>
   array (
     0 => '192.168.1.100',
     1 => 'your.ddns.domain',
   ), ``

Set up port fowarding rules on router

# Resolve Nextcloud security prompts


# Use UUID for externl HD mounting
source: https://www.cyberciti.biz/faq/linux-finding-using-uuids-to-update-fstab/

__note__ UUID changes when drives formated.

- add primary HD (plugged in)
- Use ``blkid`` command-line utility to locate/print block device attributes:

open fstab to edit
``sudo nano /etc/fstab``
add line
``UUID={YOUR-UID}    {/path/to/mount/point}               {file-system-type}    defaults,errors=remount-ro 0       1``

- add airgapped back up drive:
    - plug in drive to correct port(hijacked circuit -should not power upas relay open)
    - switch dir ``cd /NAS_drive/functions``
    - shut relay to power up 2nd HD ``python relay_power_on.py``
    - Use  ``lsblk`` - note device name (sdb1 in my case).
    - get uuid of device name with ``sudo blkid /dev/sdb1``
    -note uuid
    open fstab to edit
``sudo nano /etc/fstab``
add line
``UUID={YOUR-UID}    {/path/to/mount/point}               {file-system-type}    defaults,errors=remount-ro 0       1``

