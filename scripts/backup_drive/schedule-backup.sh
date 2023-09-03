# Write scheduled job to cron.
(crontab -l ; echo "* * * * * sh /home/scott/NAS_drive/functions/back-up.sh")| crontab -