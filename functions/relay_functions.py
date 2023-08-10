import RPi.GPIO as GPIO

RELAY_CHANNEL = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_CHANNEL, GPIO.OUT)

def power_on():
    GPIO.output(RELAY_CHANNEL, GPIO.HIGH)

def power_off():
    GPIO.output(RELAY_CHANNEL, GPIO.LOW)