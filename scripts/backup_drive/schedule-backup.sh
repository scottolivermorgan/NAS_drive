#!/bin/bash

# Write scheduled hard drive backup job to cron.
(crontab -l ; echo "0 5 * * * python /home/$UN/NAS_drive/functions/back-up.py")| crontab -