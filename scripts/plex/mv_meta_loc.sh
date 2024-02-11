# Move meta data from local SD card to exteral HD
# https://forums.plex.tv/t/howto-an-extended-guide-on-how-to-move-the-plex-data-folder-on-windows/197060
# https://forums.plex.tv/t/customizing-your-plex-configuration/205443
# intended for those systems where cat /proc/1/comm returns systemd

systemctl stop plexmediaserver

mkdir /etc/systemd/system/plexmediaserver.service.d

cd /etc/systemd/system/plexmediaserver.service.d

# create metatdata dir in custom location before below

echo "#
# Customize Plex's config
#
# Identify this as a service override
[Service]
#
#  Move the data directory
Environment="PLEX_MEDIA_SERVER_APPLICATION_SUPPORT_DIR=/media/'$PLEX_DATA_LOC'/Media/metadata"
#
#  These values are only needed if you wish to change user & group
#User=chuck
#Group=chuck
#
# This is needed to change the default umask     
UMask=0002    # this must be octal    - See warning below " >override.conf

systemctl daemon-reload

systemctl start plexmediaserver



