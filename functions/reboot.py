#!/usr/bin/env python3

#from gpiozero import Button
#import os
#
## Initiate shutdown sequence on button push
#Button(22).wait_for_press()
#os.system("sudo reboot")
#
#
##!/usr/bin/env python3

from gpiozero import Button
import RPi.GPIO as GPIO
import os
import time

# Initialize button on GPIO pin 22 and LED on GPIO pin 23
button = Button(22)

RELAY_CHANNEL = 23

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_CHANNEL, GPIO.OUT)

# Wait for button press and flash the LED
button.wait_for_press()

# Flash the LED 10 times
for _ in range(20):
    GPIO.output(RELAY_CHANNEL, GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(RELAY_CHANNEL, GPIO.LOW)
    time.sleep(0.25)

# Initiate shutdown/reboot sequence
os.system("sudo reboot")
