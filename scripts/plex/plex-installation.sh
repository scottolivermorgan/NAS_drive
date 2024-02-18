#!/bin/bash

# This script installs Plex Media Server on a Debian-based system.
# It adds the Plex repository to the package sources, installs the necessary transport-https package,
# downloads the Plex signing key, updates the package lists, and finally installs Plex Media Server.

# Exit immediately if a command exits with a non-zero status.
set -e

# Install the transport-https package, which allows the "apt" package manager to retrieve packages
# over the https protocol that the Plex repository uses.
echo "Installing transport-https"
sudo apt-get install -y apt-transport-https

# Add Plex repository to package sources.
echo "Adding Plex repository to package sources"
echo "deb https://downloads.plex.tv/repo/deb public main" | sudo tee /etc/apt/sources.list.d/plexmediaserver.list > /dev/null

# Download Plex signing key and add it to trusted keys.
echo "Downloading Plex signing key"
curl https://downloads.plex.tv/plex-keys/PlexSign.key | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/plex.gpg

# Update package lists to include Plex repository.
echo "Updating package lists"
sudo apt update

# Install Plex Media Server.
echo "Installing Plex Media Server"
sudo apt install -y plexmediaserver
