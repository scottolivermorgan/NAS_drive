#!/usr/bin/env python3

from gpiozero import Button
import os

# Initiate shutdown sequence on button push
Button(21).wait_for_press()
os.system("sudo poweroff")
