# Write scheduled job to cron.
(crontab -l ; echo "* * * * * /home/pi/NAS_drive/scripts/backup_drive/schedule-backup.sh")| crontab -

#echo "$(echo '* * * * * /NAS_drive/functions/back-up.sh' ; ssh pi@raspberrypi crontab -l 2>&1)" | ssh pi@raspberrypi "crontab -"