from dual_motor_driver import DualMotorDriver
from picozero import DistanceSensor
from machine import Pin, PWM, reset
from utime import *

motors = DualMotorDriver(right_ids=(15,13,14), left_ids=(16,18,17), stby_id= 12)
sensor = DistanceSensor(trigger = 9, echo= 8)
red = Pin(28, mode= Pin.OUT )
green = Pin(27, mode= Pin.OUT)
blue = Pin(26, mode= Pin.OUT)
button = Pin(22, Pin.IN, Pin.PULL_DOWN)

light = "green"
mode = 0
start_time = 0
accumulated_off_timer = 0
speed = .5

def toggle_mode(hi):
    global mode, start_time
    mode = mode + 1
    print("mode ->", mode)
    if mode == 1:
        start_time = ticks_ms()
    
    if mode > 1:
        mode = 0

button.irq(trigger= Pin.IRQ_FALLING, handler = toggle_mode)

def avoid_wall():
    motors.linear_backward(speed= .5)
    sleep(.4)
    motors.spin_left(speed = .5)
    sleep(.25)
    motors.linear_forward(speed = .5)

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
    if dist is not None and button.value() == 0:
        for i in range(10):
            LED('on')
            sleep(1/5)
            turn_off_leds()
    else:
        print("sensor not working")
            
            
def pause_mode(): #fades the led 
    motors.stop()
    led_pwm = PWM(green)
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
    green.init(mode= Pin.OUT)

def low_battery():
    global accumulated_off_timer
    global speed
    speed = speed / 2
    off_timer = ticks_ms()
    LED("red")
    sleep(1/5)
    turn_off_leds()
    sleep(1/5)
    accumulated_off_timer = ticks_diff(ticks_ms(), off_timer)
    if accumulated_off_timer >= 5000:
        reset()

def Desired_range(DesiredRange):
    CurrentRange = sensor.distance
    print(CurrentRange)
    if CurrentRange is None:
        return False
    isWallInRange = (DesiredRange - 0.05 <= CurrentRange <= DesiredRange + 0.05)
    #isWallInRange = (CurrentRange == DesiredRange)
    if isWallInRange:
        motors.stop()
    return isWallInRange

def work_mode():
    global start_time
    motors.linear_forward(speed = .5)
    work_time = ticks_diff(ticks_ms(), start_time)
    if Desired_range(.2):
        avoid_wall()
    if work_time < 45000:
        light = "green"
        LED(light)
    elif work_time > 45000 and work_time < 55000:
        light = "blue"
        LED(light)
    elif work_time > 55000:
        low_battery()
            
wall_detection_check()
while True:
    if mode == 0:
        pause_mode()
    if mode == 1:
        work_mode()
        
            
        
            
            
            
            
            
            