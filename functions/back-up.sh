python /home/pi/NAS_drive/functions/relay_power_on.py

sleep 20s

rsync -av /media/scott/cloudDrive/* /media/scott/cloudDriveBU

sleep 20s

python /home/pi/NAS_drive/functions/relay_power_off.py