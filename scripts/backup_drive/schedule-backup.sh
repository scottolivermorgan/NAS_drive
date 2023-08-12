# Write scheduled job to cron.
(crontab -l ; echo "* * * * * sh /home/pi/NAS_drive/functions/back-up.sh")| crontab -