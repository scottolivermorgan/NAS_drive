# Write scheduled job to cron.
(crontab -l ; echo "*/5 * * * * sh /home/scott/NAS_drive/functions/back-up.sh")| crontab -

#(crontab -l ; echo "0 */48 * * * sh /home/scott/NAS_drive/functions/back-up.sh")| crontab -