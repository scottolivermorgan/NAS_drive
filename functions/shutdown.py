#!/usr/bin/env python3
from gpiozero import Button
import RPi.GPIO as GPIO
import os
import time

# Initialize button on GPIO pin 22 and LED on GPIO pin 23
button = Button(24)

led_pin = 23

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

# Wait for button press and flash the LED
button.wait_for_press()

# Flash the LED 3 times
for _ in range(3):
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(1.)
    GPIO.output(led_pin, GPIO.LOW)
    time.sleep(1.)

# Initiate shutdown/reboot sequence
os.system("sudo shutdown")
