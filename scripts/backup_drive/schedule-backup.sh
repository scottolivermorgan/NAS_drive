# Write scheduled hard drive backup job to cron.
(crontab -l ; echo "0 */24 * * * sh /home/scott/NAS_drive/functions/back-up.sh")| crontab -