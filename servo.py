import RPi.GPIO as GPIO
import pigpio
import time

#Button = 16
servo = 13
servo1 = 12

pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)
pwm.set_mode(servo1, pigpio.OUTPUT)
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(Button, GPIO.IN)

pwm.set_PWM_frequency( servo, 50 )
pwm.set_PWM_frequency( servo1, 50 )

def right():
    print("--- Servo Right ---")
    pwm.set_servo_pulsewidth( servo, 1300 ) ;
    time.sleep( .5 )

def left():
    print("--- Servo Left ---")
    pwm.set_servo_pulsewidth( servo, 1900 ) ;
    time.sleep( .5 )
    
def up():
    print("--- Servo Up ---")
    pwm.set_servo_pulsewidth( servo1, 1150 ) ;
    pwm.set_servo_pulsewidth( servo, 1600 ) ;
    time.sleep( .5 )

def center():
    print("--- Servo Center ---")
    pwm.set_servo_pulsewidth( servo1, 1400 ) ;
    pwm.set_servo_pulsewidth( servo, 1600 ) ;
    time.sleep( .5 )

def down():
    print("--- Servo Down ---")
    pwm.set_servo_pulsewidth( servo1, 1580 ) ;
    pwm.set_servo_pulsewidth( servo, 1600 ) ;
    time.sleep( .5 )