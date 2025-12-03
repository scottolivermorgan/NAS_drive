# Modular Cron Jobs System

This directory contains bash script templates for modular cron jobs that replace the verbose inline cron entries previously used in the Ansible playbook.

## Overview

Instead of having long, complex cron job commands directly in the crontab, each maintenance task is now implemented as a separate bash script. This approach provides several benefits:

- **Maintainability**: Each script can be edited independently without affecting others
- **Readability**: Cron entries are now simple and easy to understand
- **Debugging**: Individual scripts can be tested and debugged separately
- **Reusability**: Scripts can be called from other automation tools
- **Logging**: Consistent logging and notification patterns across all jobs

## Log Management with Logrotate

All cron job logs are automatically managed by **logrotate** with configurable retention periods:

- **Retention**: Configurable via `config.yml` (default: 7 days)
- **Rotation**: Daily rotation with size-based triggers
- **Compression**: Old logs are compressed to save space
- **Permissions**: Proper ownership and permissions maintained
- **Schedule**: Logrotate runs daily at 2:00 AM

### Logrotate Configuration

The logrotate configuration is defined in `config.yml`:

```yaml
logrotate:
  # Number of days to keep log files
  log_retention_days: 7
  # Maximum size of log files before rotation
  max_size: "100M"
  # Whether to compress old log files
  compress: true
  # Whether to create new log files after rotation
  create: true
  # User and group for new log files
  user: "{{ ansible_user }}"
  group: "{{ ansible_user }}"
  # Permissions for new log files
  mode: "0644"
```

## Script Templates

### 1. `update_and_upgrade.sh.j2`
- **Purpose**: Updates package lists and upgrades installed packages
- **Schedule**: Daily at 14:20 (2:20 PM)
- **Logs**: `/home/{{ ansible_user }}/NAS_drive/logs/cron_update.log`

### 2. `clear_apt_cache.sh.j2`
- **Purpose**: Cleans APT package cache to free disk space
- **Schedule**: Daily at 04:10 (4:10 AM)
- **Logs**: `/home/{{ ansible_user }}/NAS_drive/logs/cron_clean_apt_cache.log`

### 3. `docker_cleanup.sh.j2`
- **Purpose**: Cleans up Docker containers, images, and volumes
- **Schedule**: Daily at 04:13 (4:13 AM)
- **Logs**: `/home/{{ ansible_user }}/NAS_drive/logs/docker_cleanup.log`

### 4. `journal_vacuum.sh.j2`
- **Purpose**: Removes journal logs older than 3 days
- **Schedule**: Daily at 04:15 (4:15 AM)
- **Logs**: `/home/{{ ansible_user }}/NAS_drive/logs/journal_vacuum.log`

### 5. `hd_backup.sh.j2`
- **Purpose**: Runs external hard drive backup script
- **Schedule**: Daily at 04:20 (4:20 AM)
- **Logs**: `/home/{{ ansible_user }}/NAS_drive/logs/hd_backup.log`

### 6. `daily_reboot.sh.j2`
- **Purpose**: Performs daily system reboot
- **Schedule**: Daily at 07:00 (7:00 AM)
- **Logs**: `/home/{{ ansible_user }}/NAS_drive/logs/daily_reboot.log`

### 7. `notify_new_media.sh.j2`
- **Purpose**: Scans for new media and sends notifications
- **Schedule**: Daily at 17:00 (5:00 PM)
- **Logs**: `/home/{{ ansible_user }}/NAS_drive/logs/notify_new_media.log`

## Common Features

All scripts include:
- Proper environment variable setup
- Comprehensive logging to dedicated log files
- Summary generation for notifications
- Integration with the notification server at `http://192.168.2.179:8090/routine_maintenence`
- Error handling and output capture

## Deployment

The scripts are deployed via the Ansible playbook (`tasks/cron_jobs.yml`) which:
1. Creates the necessary directories
2. Templates all script files with proper permissions (0777)
3. Sets up cron entries that call the scripts

Logrotate is configured via `tasks/logrotate.yml` which:
1. Installs logrotate package
2. Creates logrotate configuration for cron logs
3. Sets up daily log rotation at 2:00 AM
4. Tests configuration for validity

## Manual Testing

To test a script manually:
```bash
# Navigate to the cron_jobs directory
cd /home/{{ ansible_user }}/NAS_drive/functions/cron_jobs

# Make a script executable (if needed)
chmod +x script_name.sh

# Run the script
./script_name.sh
```

To test logrotate configuration:
```bash
# Test configuration (dry run)
sudo logrotate -d /etc/logrotate.d/nas_drive_cron_logs

# Force rotation (actual run)
sudo logrotate -f /etc/logrotate.d/nas_drive_cron_logs
```

## Log Locations

All cron job logs are stored in `/home/{{ ansible_user }}/NAS_drive/logs/` with descriptive names that match the script names.

Logrotate creates rotated files with date extensions (e.g., `cron_update.log-20241201.gz`) and automatically removes logs older than the configured retention period.

## Adding New Cron Jobs

To add a new cron job:
1. Create a new script template in this directory
2. Add the templating task to `cron_jobs.yml`
3. Add the cron entry task to `cron_jobs.yml`
4. Follow the established pattern for logging and notifications
5. The logrotate configuration will automatically pick up new `.log` files

## Logrotate Commands

- **Check status**: `sudo cat /var/lib/logrotate/status`
- **Test configuration**: `sudo logrotate -d /etc/logrotate.d/nas_drive_cron_logs`
- **Force rotation**: `sudo logrotate -f /etc/logrotate.d/nas_drive_cron_logs`
- **View configuration**: `sudo cat /etc/logrotate.d/nas_drive_cron_logs`
