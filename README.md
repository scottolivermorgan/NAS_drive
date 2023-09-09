TODO:
- script to automate gui config on NC
- script to automate gui config on Plex.
# Pre steps
- Rename main external hard drive to cloudDrive and back up to cloudDriveBU.
- _note_ Synch drives before setting up as MUCH quciker if large and popultated (use Free file sync).

- Ensure Hd cloudDrive is attatched to permenant usb and cloudDriveBU attatched to realy controled USB.

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
Insert SD and turn on Pi, navigate to router on local network (192.168.1.1 for me) and login to router, navigate to connected devices and find Pi address.

# Update Pi
- On network connected computer open Powershell and run the following command, if this is the first time connecting you will be prompted for ssh fingerprint, type yes.

    ``ssh <username>@192.168.1.x -v``



__Note:__ if this has been done before and is fresh installation, navigate to C://users/user/.ssh/known_hosts and delete previous fingerprint.

 - Clone this repo:
``git clone https://github.com/scottolivermorgan/NAS_drive.git``

__Note:__ if the following error occurs:
``error: RPC failed; curl 16 Error in the HTTP2 framing layer``

retry cmd, else if error persits Run:
    ``git config --global http.version HTTP/1.1``
    and re- try the clone cmd


- Update packages and reboot Pi:
``yes | sudo sh NAS_drive/scripts/update.sh``

The Pi reboots upon completion.

# New Version 03092023
- On network connected computer open Powershell & reconnect to Pi:
``ssh <username>@192.168.1.x -v``

- Run nextcloud script and follow prompts, pi user is your current user, then set nextcloud user name & passweord as prompted.
``sudo sh NAS_drive/scripts/nc.sh``

__bug note__
fstab UUID incorrect, run following cmd and note UUID of relevent drive
``blkid``

then ``sudo nano /etc/fstab``

append with  (replacing relevent UUID):
``UUID=C41E05971E0583A0    /media/hardrive1               ntfs    defaults,errors=remount-ro 0       1``


- Schedule relay for back up every 24 hours (_note_ runs in superuser cron jobs):
``sudo sh NAS_drive/scripts/backup_drive/schedule-backup.sh``

__note__ Can check cron logs with
``grep CRON /var/log/syslog``

- Edit start up scripts to run shutdown.py to listen to button
``sudo sh NAS_drive/scripts/shutdown_switch/shutdown.sh``


# Enable External Storage via GUI

~~``lsblk``     - Check mount point is sda1~~

~~``sudo sh mount-drives.sh``~~

Click top right userprofile icon and select Apps.
![addExt1](./assets/nextcloud_add_external_drive/nc1.PNG)

Scroll list and select Enable on External Storage support
![addExt1](./assets/nextcloud_add_external_drive/nc2.PNG)

Wait several seconds, again select user icon at top right and select Administrator settings.
![addExt1](./assets/nextcloud_add_external_drive/nc3.PNG)

Select External storage tab on left and add name, Local, and add mount point defined in mount-drives.sh - /media/hardrive1
![addExt1](./assets/nextcloud_add_external_drive/nc4.PNG)

Return to SSH shell and reboot Pi.
``sudo reboot``

## Plex
~~From SSH shell update packages if havent recently~~

~~``sudo sh update.sh``~~

~~Change directory to plex installation script~~
~~``cd NAS_drive/scripts/plex``~~

install plex
``sudo sh NAS_drive/scripts/plex/plex-installation.sh``

Access Plex at 192.168.1.x:32400/web -x dependant on your local network.

Sign in/create account and addexternal lib via GUI
Add Libary > harddrive1 (in this case as has been set in previouse steps)

~~# Enter Enviroment variables~~
~~On network connected computer open Powershell:~~
~~``ssh <username>@192.168.1.x -v``~~


~~run the following cmd & enter prompts to set up Nextcloud credentials.~~
~~``sudo sh NAS_drive/scripts/env_setup.sh``~~

~~``sudo sh source NAS_drive/scripts/env_setup.sh``~~





~~blkid | grep -rn 'LABEL="cloudDrive"' | grep -o ' UUID="[^"]~~*'

~~blkid | grep -rn 'LABEL="cloudDrive"' | grep -o ' UUID="[^"]*' | awk -F= '{print $2}' | tr -d '"'~~



~~export DRIVE_1_UUID=$(blkid | grep -rn 'LABEL="cloudDrive"' | grep -o ' UUID="[^"]*')~~

~~export DRIVE_1_UUID=$(blkid | grep -rn 'LABEL="cloudDrive"' | grep -o ' UUID="[^"]*' | awk -F= '{print $2}' | tr -d '"')~~






~~# Nextcloud ~~
~~On network connected computer open Powershell:~~
~~``ssh <username>@192.168.1.x -v``~~

~~Change into repo folder:~~
~~``cd NAS_drive/scripts/nextcloud``~~

~~Install nexcloud dependancies and follw prompts:~~
~~``yes | sudo sh nextcloud-dependancies.sh``~~

~~Setup initial databse and user for nextcloud, follow prompts:~~
~~``sudo sh nextcloud-setup.sh``~~

~~Install nextcloud:~~
~~``yes | sudo sh nextcloud-installation.sh``~~

~~Reboot after completeion~~
~~``sudo reboot``~~



## Backup drive
Relay wiring:

_note_ GPIOs 0-8, 14 & 15 appearhigh at boot, if connected to these pins relay will power up, connect 2nd HD then power down so don't use these pins.
__Relay__  __Pin__
__+__  =    __5v Power__ (board no# 2)
__-__  =     __Ground__   (board no# 14)
__s__  =    __GPIO 14__  (board no# 8)

![pinout](./assets/backup_setup/pi4_pinout.PNG)

~~Switch to correct dir:~~
~~``cd NAS_drive/scripts/backup_drive``~~

- Schedule relay (_note_ runs in superuser cron jobs):
``sudo sh NAS_drive/scripts/backup_drive/schedule-backup.sh``

## Add Powerdown Button
Pi dosen't ship with power off button, shutting down cleanly avoids SD card corruption so add a switch and python script to enable clean shutdowns before turing off at plug.

Use board pins __39__ (ground) and __40__ (GPIO21):
![pinout](./assets/shutdown_switch/shutdown_switch_pinout.PNG)

~~Change working directory~~
~~``cd /NAS_drive/scripts/shutdown_switch``~~

 - Edit start up scripts to run shutdown.py to listen to button
``sudo sh NAS_drive/scripts/shutdown_switch/shutdown.sh``

- Reboot Pi
``sudo reboot``

## Harden Security
~~Change working dir~~
~~`` cd NAS_drive/scripts/harden_security``~~

- Install packages to auto update security patchs
``yes | sudo sh NAS_drive/scripts/harden_security/auto_patch.sh``

__Note:__ SSH port changed from 22 to 1111

~~Check for users with empty passwords~~
~~``sudo awk -F: '($2 == "") {print}' /etc/shadow``~~

~~Lock any applicable accounts~~
~~``passwd -l <username>``~~

~~Check expected logins~~
~~``lslogins -u``~~

~~Check any unexpected services running~~
~~``sudo service --status-all``~~

~~Check SHH root login disabled~~
~~``sudo nano /etc/ssh/sshd_config``~~

~~Verify following exists~~
~~``#PermitRootLogin prohibit-password``~~

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
- The PHP memory limit is below the recommended value of 512MB
``sudo nano /etc/php/8.1/apach2/php.ini``
change line:

``memory_limit = 128M``
to
``memory_limit = 1G``

# Use UUID for externl HD mounting
~~source: https://www.cyberciti.biz/faq/linux-finding-using-uuids-to-update-fstab/~~

~~__note__ UUID changes when drives formated.~~

~~- add primary HD (plugged in)~~
~~- Use ``blkid`` command-line utility to locate/print block device attributes:~~

~~open fstab to edit~~
~~``sudo nano /etc/fstab``~~
~~add line~~
~~``UUID={YOUR-UID}    {/path/to/mount/point}               {file-system-type}    defaults,errors=remount-ro 0       1``~~

~~- add airgapped back up drive:~~
    ~~- plug in drive to correct port(hijacked circuit -should not power upas relay open)~~
    ~~- switch dir ``cd /NAS_drive/functions``~~
    ~~- shut relay to power up 2nd HD ``python relay_power_on.py``~~
    ~~- Use  ``lsblk`` - note device name (sdb1 in my case).~~
    ~~- get uuid of device name with ``sudo blkid /dev/sdb1``~~
    ~~-note uuid~~
    ~~open fstab to edit~~
~~``sudo nano /etc/fstab``~~
~~add line~~
~~``UUID={YOUR-UID}    {/path/to/mount/point}               {file-system-type}    defaults,errors=remount-ro 0       1``~~

~~#Sync external HD;s~~

~~rsync syntax ~~
~~``# rsync options source destination``~~

~~``rsync -av /media/scott/cloudDrive/* /media/scott/cloudDriveBU``~~

~~test~~
~~``for i in {1..50}; do touch "testfile$i.txt"; done``~~

# Create Backup Image of Pi SD
Download & install imaging software:
https://sourceforge.net/projects/win32diskimager/

- Open Win32 Disk Imager

![WI1](./assets/SD_backup/wI_1.PNG)

![WI2](./assets/SD_backup/wI_2.PNG)

![WI3](./assets/SD_backup/wI_3.PNG)

![WI4](./assets/SD_backup/wI_4.PNG)