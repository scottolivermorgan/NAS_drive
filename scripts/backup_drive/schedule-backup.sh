#!/bin/bash

# Write scheduled hard drive backup job to cron.
(crontab -l ; echo "USER=$UN")| crontab -
(crontab -l ; echo "0 5 * * * python /home/$UN/NAS_drive/functions/back-up.py >> /home/$UN/NAS_drive/logs/back_up-cron.log 2>&1")| crontab -