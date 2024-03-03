#!/bin/bash

# Define the configuration file path
config_file="/etc/apt/apt.conf.d/50unattended-upgrades"

# Define the schedule time
schedule_time="04:00"

# Check if the configuration file exists
if [ ! -f "$config_file" ]; then
    echo "Error: UnattendedUpgrades configuration file not found at $config_file"
    exit 1
fi

# Add the schedule time to the configuration file
if grep -q "Unattended-Upgrade::Automatic-Reboot-Time" "$config_file"; then
    # Update the existing schedule time
    sed -i "s/^.*Unattended-Upgrade::Automatic-Reboot-Time.*$/Unattended-Upgrade::Automatic-Reboot-Time \"$schedule_time\";/" "$config_file"
else
    # Add the schedule time if it doesn't exist
    echo "Unattended-Upgrade::Automatic-Reboot-Time \"$schedule_time\";" | sudo tee -a "$config_file" >/dev/null
fi

# Restart the unattended-upgrades service
sudo systemctl restart unattended-upgrades

echo "UnattendedUpgrades scheduled to run at $schedule_time every day."
