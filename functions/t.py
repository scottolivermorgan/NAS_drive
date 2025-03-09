#import time
#import RPi.GPIO as GPIO
#
#
#RELAY_CHANNEL = 23
#
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(RELAY_CHANNEL, GPIO.OUT)
#
#
## Flash the LED 10 times
#for _ in range(20):
#    GPIO.output(RELAY_CHANNEL, GPIO.HIGH)
#    time.sleep(0.25)
#    GPIO.output(RELAY_CHANNEL, GPIO.LOW)
#    time.sleep(0.25)

from gpiozero import Button, LED
import os
import time

# Initialize button on GPIO pin 22 and LED on GPIO pin 23
button = Button(22)
led = LED(23)

# Function to flash the LED 20 times
def flash_led():
    for _ in range(20):
        led.on()
        time.sleep(0.25)
        led.off()
        time.sleep(0.25)

flash_led()