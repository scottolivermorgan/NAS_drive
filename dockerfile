# Use the official Ubuntu 20.04 image as the base image
FROM ubuntu:20.04

# Set environment variables to prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install Git and Python
RUN apt-get update && \
    apt-get install -y git python3 && \
    apt-get clean

# Create a user named "scott" with a home directory
RUN useradd -m -s /bin/bash scott

# Set the default user to "scott"
USER scott

# Set the working directory to the home directory of the "scott" user
WORKDIR /home/scott

# Clone the Git repository and switch to dev branche
RUN git clone https://github.com/scottolivermorgan/NAS_drive.git && \
    cd NAS_drive && \
    git fetch --all && \
    git checkout origin/extend_HD
