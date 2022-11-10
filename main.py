# Kode starter, Venter på knap, knap trykkes "camCode.py" køres,
# servo motorer kode kører og det fortsætter indtil nok billeder er taget fra et sted
#
# Når alle billeder er taget, holdes knappen inde i 5 sekunder, derefter
# vil alle billederne sendes til serveren med Mechroom

import time
import os
from RPi import GPIO

while True:
    if GPIO.input(butt) == GPIO.LOW:
        print("Button pressed...")
        os.system('python /home/pi/Desktop/code/camCode.py')