from time import sleep
from picamera import PiCamera

camera = PiCamera()
#camera.start_preview()
#sleep(0.2) # Sleep to let the camera warm up
#start = 0
#slut = 4 # Change the number of images taken

def takePic(slut):
    start = 0
    for i in camera.capture_continuous("/home/pi/Desktop/pics/img{timestamp:%H%M%S}-{counter:03d}.jpg"):
        print("Captured %s" % i)
        start = start+1
        print(start,"image(s) captured out of",slut)
        #sleep(1)
        if start == slut:
            break