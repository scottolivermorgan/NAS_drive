import time
import RPi.GPIO as GPIO


RELAY_CHANNEL = 23

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_CHANNEL, GPIO.OUT)


# Flash the LED 10 times
for _ in range(10):
    GPIO.output(RELAY_CHANNEL, GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(RELAY_CHANNEL, GPIO.LOW)
    time.sleep(0.25)