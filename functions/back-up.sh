echo "Closing airgap"

python /home/$USER/NAS_drive/functions/relay_power_on.py

echo "Mounting hard drive"

sleep 20s

echo "Syncing drives"

rsync -av --log-file="/home/$USER/NAS_drive/logs/sync_log.log" /media/hardrive1/* /media/scott/cloudDriveBU 

sleep 20s

echo "Closing airgap"

python /home/$USER/NAS_drive/functions/relay_power_off.py