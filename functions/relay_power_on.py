import RPi.GPIO as GPIO

def power_on():
    GPIO.output(RELAY_CHANNEL, GPIO.HIGH)

if __name__ == "__main__":
    RELAY_CHANNEL = 18
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_CHANNEL, GPIO.OUT)
    power_on()