# download the library to your home directory.
wget http://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.7.1.tar.gz

# Extract the contents
tar xvzf RPi.GPIO-0.7.1.tar.gz

# Change to the newly created directory
cd RPi.GPIO-0.7.1

# Install the library into Python
sudo python setup.py install

# Remove the directory and its contents
cd ..

rm -rf RPi.GPIO-0.7.1/

# Delete the archive file
rm Rpi.GPIO-0.7.1.tar.gz