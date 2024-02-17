# Install tansport-https package, allows the “apt” package manager to retrieve packages 
# over the https protocol that the Plex repository uses.
echo "Installing transport-https"
apt-get install apt-transport-https

echo deb https://downloads.plex.tv/repo/deb public main | sudo tee /etc/apt/sources.list.d/plexmediaserver.list
curl https://downloads.plex.tv/plex-keys/PlexSign.key | sudo apt-key add -

echo "Installing plexmediaserver"
apt update
apt install plexmediaserver

echo "Checking plex server status"
sudo systemctl status plexmediaserver


# Add the Plex repositories to the “apt” keyrings directory.


#echo "Adding Plex repos to keyrings dir"
#curl https://downloads.plex.tv/plex-keys/PlexSign.key | gpg --dearmor | tee /usr/share/keyrings/plex-archive-keyring.gpg >/dev/null

# Add the official plex repository to the sources list.


#echo deb [signed-by=/usr/share/keyrings/plex-archive-keyring.gpg] https://downloads.plex.tv/repo/deb public main | tee /etc/apt/sources.list.d/plexmediaserver.list

# Refresh the package list.


#apt-get update

# Install the “plexmediaserver” package


#apt install plexmediaserver

# creates a user and group for Plex to run under. This user and group is called “plex“.
# it also will set up two directories, one where to store files temporarily that Plex 
# is transcoding. You can find this folder at “/var/lib/plexmediaserver/tmp_transcoding“.

# second directory is where Plex will store all the metadata it retrieves for your media.
# This folder can be found at “/var/lib/plexmediaserver/Library/Application Support