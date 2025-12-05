"""
Rush the robot to a wall, stop at the required distance
"""

#Right motor pins
#in1 = 9, in2 = 11, PWM = 10

#left motor pins
#in1 = 15, in2 = 13, PWM = 14

# standby pin = 12

#sensor trigger pin = 1
#sensor echo pin = 2
#RGB led pin = 5,6,7

from machine import Pin
from picozero import DistanceSensor
from dual_motor_driver import DualMotorDriver
from time import sleep

motor = DualMotorDriver(right_ids=(10, 11, 9), left_ids=(14, 15, 13), stby_id=12)
sensor = DistanceSensor(trigger= 1, echo = 2)
red = Pin(5, mode= Pin.OUT )
green = Pin(6, mode= Pin.OUT)
blue = Pin(7, mode= Pin.OUT)
first = False
second = False
third = False
fourth = False
print("program starting")

def turn_off_leds():
    red.off()
    blue.off()
    green.off()

def LED(color):
    turn_off_leds()
    if color == 'red':
        red.on()
    elif color == 'blue':
        blue.on()
    elif color == 'green':
        green.on()
    elif color == 'on':
        red.on()
        blue.on()
        green.on()

        
def wall_detection_check():
    dist = sensor.distance
    if dist != None:
        for i in range(10):
            LED('on')
            sleep(1/5)
            LED('off')
            first = True
            
def drive_backwards():
    motor.linear_backward(.5)
    LED('blue')

def drive_stop():
    LED("red")
    motor.stop()
    sleep(1)

def drive_forward():
    motor.linear_forward(.5)
    LED('green')

def Desired_range(DesiredRange):
    CurrentRange = sensor.distance
    isWallInRange = (DesiredRange - 0.05 <= CurrentRange <= DesiredRange + 0.05)
    #isWallInRange = (CurrentRange == DesiredRange)
    if isWallInRange:
        drive_stop()
    return isWallInRange
        
wall_detection_check()
first = True

while first:
    drive_forward()
    if Desired_range(.25):
        second = True
        first = False
while second:
    drive_backwards()
    if Desired_range(1):
        third = True
        second = False
while third:
    drive_forward()
    if Desired_range(.25):
        fourth = True
        third = False
while fourth:
    drive_backwards()
    if Desired_range(.5):
        fourth = False