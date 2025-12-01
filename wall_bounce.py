from dual_motor_driver import DualMotorDriver
from picozero import DistanceSensor
from machine import Pin, PWM
from utime import *

motors = DualMotorDriver(right_ids=(10,9,11), left_ids=(14.13,15), stby_id= 12)
sensor = DistanceSensor(trigger = 21, echo= 22)
red = Pin(5, mode= Pin.OUT )
green = Pin(6, mode= Pin.OUT)
blue = Pin(7, mode= Pin.OUT)
button = Pin(19, Pin.IN, Pin.PULL_DOWN)
mode = 0



def avoid_wall():
    motors.linear_backward(speed= 1)
    sleep(1)
    motors.spin_left(speed = 1)
    sleep(1)
    motors.linear_forward(speed = 1)

def turn_off_leds():
    red.off()
    blue.off()
    green.off()
 
 
#handles LED color    
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
      
#checks if sensor is reading and checks if button works        
def wall_detection_check(): 
    dist = sensor.distance
    if dist != None and button.value == 0:
        for i in range(10):
            LED('on')
            sleep(1/5)
            LED('off')
            first = True
            
def pause_mode(led): #fades the led 
    motors.stop()
    led_pwm = PWM(led)
    led_pwm.freq(1000)
    steps = 256
    step_delay_us = int((500000) / (65535 / steps))
    # fade in
    for i in range(0, 65536, steps):
        if mode != 0:
            break
        led_pwm.duty_u16(i)
        sleep_us(step_delay_us)
    # fade out
    for i in range(65535, -1, -steps):
        if mode != 0:
            break
        led_pwm.duty_u16(i)
        sleep_us(step_delay_us)
    led_pwm.deinit()

def low_battery():
    LED("red")
    sleep()
    
def Desired_range(DesiredRange):
    CurrentRange = sensor.distance
    isWallInRange = (DesiredRange - 0.05 <= CurrentRange <= DesiredRange + 0.05)
    #isWallInRange = (CurrentRange == DesiredRange)
    if isWallInRange:
        motors.stop
    return isWallInRange    

def work_mode():
    LED("green")
    motors.linear_forward(speed = 1)
    while True:
        start = ticks_ms()
        work_time += ticks_diff(ticks_ms(), start)
        if Desired_range(.25):
            avoid_wall()
        if work_time > 45000:
            LED("blue")
        if work_time > 55000:
            
            
        
            
            
            
            
            
            