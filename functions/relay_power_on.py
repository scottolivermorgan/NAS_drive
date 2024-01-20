import RPi.GPIO as GPIO
import time
from helpers import pre_sync_hash_verification, power_on
import json

fp = "C:\\Users\\Scott\\projects\\NAS_drive\\config.json"

# Open and read the config.json file
with open(fp, 'r') as config_file:
    config_data = json.load(config_file)


# Iterate over external hard drive mappings
for index, hd_obj in enumerate(config_data['HD_map']):

    if pre_sync_hash_verification():
        print('Verification sucsessfull')

        # Extract the "GPIO_pin" parameter from the configuration
        RELAY_CHANNEL = config_data['HD_map'][hd_obj]['GPIO_pin']

        # Confi pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RELAY_CHANNEL, GPIO.OUT)

        # power up relay
        power_on(RELAY_CHANNEL)
    else:
        print('Verification failed')






"""

if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)

    GPIO.output(18, GPIO.HIGH)
    time.sleep(10)
    GPIO.output(18, GPIO.LOW)
    time.sleep(5)

    GPIO.output(17, GPIO.HIGH)
    time.sleep(10)
    GPIO.output(17, GPIO.LOW)



 
"""
