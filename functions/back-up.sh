echo "Closing airgap"

python /home/scott/NAS_drive/functions/relay_power_on.py

echo "Mounting hard drive"

sleep 20s

echo "Syncing drives"

rsync -av /media/scott/cloudDrive/* /media/scott/cloudDriveBU

sleep 20s

echo "Closing airgap"

python /home/scott/NAS_drive/functions/relay_power_off.py