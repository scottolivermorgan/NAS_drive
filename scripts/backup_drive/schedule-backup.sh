# Write scheduled job to cron.
#(crontab -l ; echo "* * * * * /NAS_drive/functions/back-up.sh")| crontab -

echo "$(echo '* * * * * /NAS_drive/functions/back-up.sh' ; ssh pi@raspberrypi crontab -l 2>&1)" | ssh pi@raspberrypi "crontab -"