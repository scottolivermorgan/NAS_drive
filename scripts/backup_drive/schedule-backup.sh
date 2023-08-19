# Write scheduled job to cron.
(crontab -l ; echo "* * * * * sh /home/$UN/NAS_drive/functions/back-up.sh")| crontab -