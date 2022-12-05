#!/usr/bin/env python3

import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# There are 16 channels on the PCA9685 chip.
kit = ServoKit(channels=16)

# Name and set up the servo according to the channel you are using.
servo = kit.servo[0]
print(servo)

# Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
# Each servo might be different, you can normally find this information in the servo datasheet
servo.set_pulse_width_range(500, 2500)


def open_lid():
    servo.angle = 120


def close_lid():
    servo.angle = 0


while True:
    cmd = input("> ")
    if cmd == "o":
        open_lid()
    elif cmd == "c":
        close_lid()
    else:
        exit(0)
