# Use the official Ubuntu 20.04 image as the base image
FROM ubuntu:20.04

# Set environment variables to prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install Git, Python, sudo, and pip
RUN apt-get update && \
    apt-get install -y git sudo nano && \
    apt install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    apt-get install -y python3.9 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a user named "scott" with a home directory and give sudo privileges
RUN useradd -m -s /bin/bash scott && \
    echo "scott ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/scott && \
    chmod 0440 /etc/sudoers.d/scott

# Set the default user to "scott"
USER scott

# Set the working directory to the home directory of the "scott" user
WORKDIR /home/scott

# Clone the Git repository and switch to the "extend_HD" branch
RUN git clone https://github.com/scottolivermorgan/NAS_drive.git && \
    cd NAS_drive && \
    git fetch --all && \
    git checkout origin/extend_HD

# Install Python dependencies from requirements.txt
RUN pip3 install --user -r NAS_drive/requirements.txt

# Set the default command when the container is run
CMD ["/bin/bash"]
