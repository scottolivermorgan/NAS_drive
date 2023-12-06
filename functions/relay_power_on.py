import RPi.GPIO as GPIO
from helpers import pre_sync_hash_verification

def power_on():
    GPIO.output(RELAY_CHANNEL, GPIO.HIGH)

if __name__ == "__main__":
    if pre_sync_hash_verification():
        RELAY_CHANNEL = 18
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RELAY_CHANNEL, GPIO.OUT)
        power_on()
    else:
        print('Verification failed')

