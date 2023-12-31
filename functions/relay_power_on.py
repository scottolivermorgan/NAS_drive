import RPi.GPIO as GPIO
from helpers import pre_sync_hash_verification

def power_on() -> None:
    """
    Turns on the power by setting the GPIO output to high for the specified relay channel.

    This function uses the GPIO library to control a relay channel, turning it on by setting the
    corresponding GPIO output to high.

    Note:
    Make sure to initialize the GPIO setup before calling this function.

    Example:
    ```python
    # Set up GPIO (assumed to be done before calling power_on)
    GPIO.setup(RELAY_CHANNEL, GPIO.OUT)

    # Turn on the power
    power_on()
    ```

    Raises:
        Any exceptions raised by the GPIO library during the output setting.

    Global Constants:
        - RELAY_CHANNEL: The GPIO channel connected to the relay.

    """
    GPIO.output(RELAY_CHANNEL, GPIO.HIGH)

if __name__ == "__main__":
    if pre_sync_hash_verification():
        print('Verification sucsessfull')
        RELAY_CHANNEL = 18
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RELAY_CHANNEL, GPIO.OUT)
        power_on()
    else:
        print('Verification failed')

