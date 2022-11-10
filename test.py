import servo as servo
import camCode
from time import sleep

def camRoutine():
    print('Starting taking pictures..')
    servo.center()
    camCode.takePic(1)
    servo.right()
    camCode.takePic(1)
    servo.left()
    camCode.takePic(1)
    servo.up()
    camCode.takePic(1)
    servo.down()
    camCode.takePic(1)
    servo.center()
    print('Done!')

camRoutine()
