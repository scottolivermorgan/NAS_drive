import os
import json
import sys
import time
import RPi.GPIO as gpio

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from library.helpers import power_on

power_on(18, ON=True)
time.sleep(20)
power_on(18, ON=False)

power_on(17, ON=True)
time.sleep(20)
power_on(17, ON=False)