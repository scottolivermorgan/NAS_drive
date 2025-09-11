#TODO uv instructions to readme + migrate



# What
- sets up rasberry pi as a media server in one command.
- scalable storage, automatically comibines external hard drives into logical volumes, one as main one as backup and syncs them every day.
- uses ARR stack to automate monitoring & downloads as they are relesed.
- Uses NTFY to send push notifications when you have new media, routine mainenece & back ups carried out.
- Uses grafana for monitering Dashboard.
- quick (about 10 mins excluding download time), easy set up, just format some external hard drives,
 set some passwords in the config file, run ansible & do some minor setup via GUI for the services.
 - this is step by step guid from scratch, don't worry if you've never touched this stuff before!

# blurb:
This project uses Ansible to set up various docker services on a rasberry pi. Ansible is an open-source automation tool that helps IT teams manage, configure, and deploy software to multiple systems efficiently by using simple, human-readable YAML playbooks—without requiring agents on the target machines, making it ideal for tasks like provisioning servers, managing configurations, orchestrating workflows, and automating repetitive tasks across large-scale environments.

# Hardware requirements:
- Rasberry pi 4b 8gb RAM.
- Raspberry Pi power supply - get the official one, Pi's can be VERY finiky if the supply is slightly off!
- an even number of external Hard drives/USB drives (4 usb's is ideal to test things with, if you like it bang some chunky HD's and re run!)
- 1 x SD card (min 32GB), i'd have three, one for developing/playing, one for productions and one as a backup.
- (Optional) HDMI cable - usefull for debugging things if you can't connect va SSH for any reason.
- (Optional) wired usb keyboard - as above.
- (Optional) 3D Printer - who dosen't want a snazzy looking case?
- (Optional) 1 LED, 1 220 Ohm resistor, small bit of bread board, 2 x switches, 4 cables and a soldering iron - The Pi 4 dosen't have
an on/off or reboot switch. Sometimes it just needs a reboot and its nice to have a switch, otherwise you have to ssh into it and run sudo reboot which is irritating when you just want to crack on & watch spongebob square pants!

### Config your computer - control node
Ansible connects your laptop to your pi via ssh and sets everything up for you but first off we need to get some software we need, only need to do this once. You can check if you already have any of this by typing in the windows search bar in the bottom left, if not:

SD card formatter:
While your default OS works in a pinch, using the SD Formatter is safer if you're preparing a card for something more than basic file storage.
https://www.sdcard.org/downloads/formatter/

Rasberry Pi imager:
For writting the rasberry pi OS to the SD card
https://www.raspberrypi.com/software/

Rasberry Pi OS image:
select raspios_lite_arm64-2024-07-04/ this will be updated as new OS become availible, but just in case any braking changes are introduced pick this one.
https://downloads.raspberrypi.com/raspios_lite_arm64/images/

VS code (optional):
For editing the config file, having terminal all in one place, lots of great features!
https://code.visualstudio.com/


Windows Only:
Ansible only works on linux distro's but this isn't an issue if your a Windows user, we just need to get Windows Substac for Linux (WSL):
- Open PowerShell or Windows Command Prompt in administrator mode by right-clicking and selecting "Run as administrator" & run
`wsl --install`
Official guide is here:
WSL https://learn.microsoft.com/en-us/windows/wsl/install


Once all the above is downloaded and installed you MUST restart your machine!


- Install ansible
`sudo apt-add-repository ppa:ansible/ansible`
`sudo apt update`
`sudo apt install ansible`

Clone this repo
`git clone https://github.com/scottolivermorgan/NAS_drive.git && cd NAS_drive`

clone `inventory.yml.example` rename to `inventory.yml` & add your name and Pi IP address - you can find this by loggin into your router.

clone `main.yml.example` rename to `main.yml` & add your git email & name. Update passwords and user name from `test`

if python venv not installed then
`sudo apt install python3.12-venv`

create virtual env
`python3 -m venv .venv`

activate it with
`source .venv/bin/activate`

You need to install for that use:
`pip install -r requirements.txt`

~~`ansible-galaxy collection install -r requirements.yml --force`~~

~~Get host IP~~
~~`sudo apt install net-tools`~~
~~`ifconfig`~~

## Initial Pi 4 Setup
Download SD card formating software:
https://www.sdcard.org/downloads/formatter/

Format card on local machine:

![formatSD](./assets/pi_setup/format_SD.png)

Download Raspberry Pi Imager:
https://www.raspberrypi.com/software/

Run Raspberry Pi Imager and flash the OS we downloaded in the previous step raspios_lite_arm64-2024-07-04/, you''l need to scroll to the bottom and select other, it's probaly then in your downloads folder.

Select settings (cog wheel - lower right)

![formatSD](./assets/pi_setup/imager_screen_1.png)

Select 'Enable shh'
Select 'Use password authentication'
'set authorised keys' auto fills to local user.
enter username and password. __DO NOT USE DEFAULT USERNAME & PASSWORDS__.

![formatSD](./assets/pi_setup/imager_screen_2.png)

Select 'Configure wireless LAN option and enter network details.
![formatSD](./assets/pi_setup/imager_screen_3.png)

Local settings auto filled, if not complete.
![formatSD](./assets/pi_setup/imager_screen_4.png)

Set hotsname as Pi, enable SSH and select use password authentication.
![formatSD](./assets/pi_setup/pialt.png)

Save and write SD, takes a few minutes.
Insert SD and turn on Pi and wait a few minutes.

# Configure external Hard drives/USBs
- Rename main external hard drive to HD_1 and back up to BU_1, follow ths convention
for all subsequent drives and add these details to config.yml (default for 4 drives, contain HD_1, HD_2, BU_1, BU_2)
# __IMPORTANT__ DO NOT USE HARD DRIVES WITH DATA ON THEM__
These ansible playbooks set up logical volumes and format them as part of the setup process
__you will loose any data on them!__
~~(alongsde the signal pin) to config.json.~~
~~Make a dir to store Plex metadata on HD_1 i.e. HD_1/Media/metadata.~~

~~- Ensure HD_1 is attatched to permenant usb and BU_1 attatched to realy controlled USB.~~


## First debug the connection:
On the laptop:
 copy ssh keys, created when you flashed the Pi OS, from windows to WSL ubuntu and update perms - they will likely be in `c:/Users/<User>/.ssh/id_rsa` copy them to `/home/<user>/.ssh/id_rsa` and in the wsl terminal run:
`chmod 600 /home/<user>/.ssh/id_rsa`

- Now change into the directory you cloned from git earlier

`cd ansible`
~~ensure .shh/.... empty first~~ 
Test the connection, the first time you do this you should be prompted to fingerprint the ssh keys, type `y` followed by enter.
`ansible-playbook -i inventory.yml debug.yml`

If everything works, run the full suite:

`ansible-playbook -i inventory.yml main.yml -vv`
after a few mins you will be prompted to copy paste a git ssh key, do this. after a few more mins you will be prompted to check you want to format each hard drive, type `y` followed by enter both times (__see warning above__). The full stack then takes about 40 mins to pull and set up all the images/services - go have a beer!
Sometimes the playbooks fail with timeouts ect on pulling images, Ansible is idempotent so just rerun the above command!


# Enable External Storage via GUI
Access nextcloud at 192.169.1.x/nextcloud fill out form adding user and usng
database user and password set in terminal prompts with  database name nextclouddb.
Browser will return error message once set up, vistit 192.169.1.x/nextcloud and:

Click top right userprofile icon and select Apps.
![addExt1](./assets/nextcloud_add_external_drive/nc1.png)

Scroll list and select Enable on External Storage support
![addExt1](./assets/nextcloud_add_external_drive/nc2.png)

Wait several seconds, again select user icon at top right and select Administrator settings.
![addExt1](./assets/nextcloud_add_external_drive/nc3.png)

Select External storage tab on left and add name, Local, and add mount point defined in mount-drives.sh - /media/hardrive1
![addExt1](./assets/nextcloud_add_external_drive/nc4.png)

# NTFY
subscriptions:
- backup_status
- media_updated
- routine_maintenence

##
Arr
https://www.youtube.com/watch?v=1eDUkmwDrWU


##TODO
  - DATA:
   - HD:
    - verify and validate komga
  Codebase:
   - fix off switch  (root?)
  - Airgap:
  - General:
   - improve/centralise/document ALL logging.




## Log Locations Reference
cron hard drive back up logs found at `/home/<USER>/NAS_drive/logs/back_up_cron.log`

## Docker Container Logs
In terminal on device `docker logs <CONTAINER_NAME>`
eg:
jellyfin:
`docker logs jellyfin`
nextcloud:
`docker logs nextcloud`
mariadb:
`docker logs mariadb`
komga:
`docker logs komga`




# Versions
### OS:
- Raspberry Pi OS Lite
- Release date: July 4th 2024
- System: 64-bit
- Kernel version: 6.6
- Debian version: 12 (bookworm)
### Nextcloud
- FE - nextcloud:29.0.2
- BE - mariadb:11.4.2
### Jellyfin
- jellyfin:latest
### Glances
- docker.io/nicolargo/glances
### Komga
- gotson/komga:latest
### Immich
 - v1.118.2
 - immich-server:v1.103.1
### Audiobookshelf
- 2.15.0

### qbittorrent
 - version-5.0.3-r0
# Serices
- Audiobookshelf - http://192.168.2.179:13378

- Bazarr - http://192.168.2.179:6767

- Glances - http://192.168.2.179:61208

- Grafana - http://192.168.2.179:3001

- Immich - http://192.168.2.179:2283

- InfluxDB - http://192.168.2.179:8086

- Jellyfin - http://192.168.2.179:8096

- Komga - http://192.168.2.179:25600

- Nextcloud - http://192.168.2.179:8000

- Prowlarr - http://192.168.2.179:9696/

- qbittorrent - http://192.168.2.179:9080

- Radarr - http://192.168.2.179:7878

- Sonarr - http://192.168.2.179:8989

- Tandoor - http://192.168.2.179:8081

- NTFY - http://192.168.2.179:8090









Relay wiring:

_note_ GPIOs 0-8, 14 & 15 appearhigh at boot, if connected to these pins relay will power up, connect 2nd HD then power down so don't use these pins.
__Relay__  __Pin__
__+__  =    __5v Power__ (board no# 2)
__-__  =     __Ground__   (board no# 14)
__s__  =    __GPIO 14__  (board no# 8)

![pinout](./assets/backup_setup/pi4_pinout.png)


## Add Powerdown Button
Pi dosen't ship with power off button, shutting down cleanly avoids SD card corruption so add a switch and python script to enable clean shutdowns before turing off at plug.

Use board pins __39__ (ground) and __40__ (GPIO21):
![pinout](./assets/shutdown_switch/shutdown_switch_pinout.png)


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

# Create Backup Image of Pi SD
Download & install imaging software:
https://sourceforge.net/projects/win32diskimager/

- Insert SD card from Pi & Open Win32 Disk Imager, check drive letter and select under device dropdown:
![WI1](./assets/SD_backup/wI_1.png)

- Select folder icon to select save location for image:
![WI2](./assets/SD_backup/wI_2.png)

- In pop up navigate to desired save location and enter  desired image name, ensure file extenino is .img
![WI3](./assets/SD_backup/wI_3.png)

Select read option to save, operation can take 10 -20 mins.
![WI4](./assets/SD_backup/wI_4.png)
