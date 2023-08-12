# Write scheduled job to cron.
(crontab -l ; echo "* * * * * /NAS_drive/functions/back-up.sh")| crontab -