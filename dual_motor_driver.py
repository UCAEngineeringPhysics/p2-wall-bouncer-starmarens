from motor_driver import MotorDriver
from machine import Pin

class DualMotorDriver:
    def __init__(self, right_ids: tuple, left_ids: tuple, stby_id: int) -> None:
        self.right_motor = MotorDriver(*right_ids)  # unzip right_pins then feed to MotorDriver
        self.left_motor = MotorDriver(*left_ids)  # unzip left_pins then feed to MotorDriver
        self.stby_pin = Pin(stby_id, Pin.OUT)
        self.enable()  # enable motor driver

    def enable(self):
        self.stby_pin.on()

    def disable(self):
        self.stby_pin.off()

    def stop(self):
        self.right_motor.stop()
        self.left_motor.stop()

    def linear_forward(self, speed=0.):
        assert 0<=speed<=1
        self.right_motor.forward(speed)
        self.left_motor.forward(speed)

    def linear_backward(self, speed=0.):
        assert 0<=speed<=1
        self.right_motor.backward(speed)
        self.left_motor.backward(speed)

    def spin_left(self, speed=0.):
        assert 0<=speed<=1
        self.right_motor.forward(speed)
        self.left_motor.backward(speed)

    def spin_right(self, speed=0.):
        assert 0<=speed<=1
        self.right_motor.backward(speed)
        self.left_motor.forward(speed)


# TEST
if __name__=="__main__":
    from time import sleep
    # SETUP
    dmd = DualMotorDriver(right_ids=(9, 11, 10), left_ids=(15, 13, 14), stby_id=12)
    
    # LOOP
    # Forward ramp up and down
    for i in range(100):
        dmd.linear_forward((i + 1) / 100)
        print(f"f, dc: {i}%")
        sleep(4 / 100)  # 4 seconds to ramp up
    for i in reversed(range(100)):
        dmd.linear_forward((i + 1) / 100)
        print(f"f, dc: {i}%")
        sleep(4 / 100)  # 4 seconds to ramp down
    # Backward ramp up and down
    for i in range(100):
        dmd.linear_backward((i + 1) / 100)
        print(f"b, dc: {i}%")
        sleep(4 / 100)  #  4 seconds to ramp up
    for i in reversed(range(100)):
        dmd.linear_backward((i + 1) / 100)
        print(f"b, dc: {i}%")
        sleep(4 / 100)  #  4 seconds to ramp down
    # Left ramp up and down
    for i in range(100):
        dmd.spin_left((i + 1) / 100)
        print(f"l, dc: {i}%")
        sleep(4 / 100)  #  4 seconds to ramp up
    for i in reversed(range(100)):
        dmd.spin_left((i + 1) / 100)
        print(f"l, dc: {i}%")
        sleep(4 / 100)  #  4 seconds to ramp down
    # Right ramp up and down
    for i in range(100):
        dmd.spin_right((i + 1) / 100)
        print(f"r, dc: {i}%")
        sleep(4 / 100)  #  4 seconds to ramp up
    for i in reversed(range(100)):
        dmd.spin_right((i + 1) / 100)
        print(f"r, dc: {i}%")
        sleep(4 / 100)  #  4 seconds to ramp down

    # Terminate
    dmd.stop()
    print("motors stopped.")
    sleep(0.1)  # full stop
    dmd.disable()  # disable motor driver
    print("motor driver disabled.")
