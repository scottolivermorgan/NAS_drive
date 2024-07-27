#!/usr/bin/env python3

from gpiozero import Button
import os
import signal
import sys

# Define a clean exit handler
def exit_gracefully(signum, frame):
    print("Cleaning up GPIO and exiting.")
    button.close()
    sys.exit(0)

# Register the clean exit handler
signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)

# Set up the button on GPIO pin 21
button = Button(21)

try:
    # Initiate shutdown sequence on button push
    button.wait_for_press()
    os.system("sudo poweroff")
finally:
    # Clean up the GPIO pin
    button.close()


#from gpiozero import Button
#import os
#
## Initiate shutdown sequence on button push
#Button(21).wait_for_press()
#os.system("sudo poweroff")
