import qwiic_led_stick
import time
import sys

my_stick = qwiic_led_stick.QwiicLEDStick()

if my_stick.begin() == False:
    print("\nThe Qwiic LED Stick isn't connected to the sytsem. Please check your connection", \
        file=sys.stderr)

print("\nLED Stick ready!")

while True:
    color=input("> ")
    if color == "r":
        my_stick.set_all_LED_color(100, 0, 0)
    elif color == "g":
        my_stick.set_all_LED_color(0, 100, 0)
    elif color == "b":
        my_stick.set_all_LED_color(0, 0, 100)
    elif color == "w":
        my_stick.set_all_LED_color(100, 100, 100)
    elif color == "bl":
        my_stick.set_all_LED_color(0, 0, 0)
    elif color == "y":
        my_stick.set_all_LED_color(100, 100, 0)
    elif color == "p":
        my_stick.set_all_LED_color(100, 0, 100)
    elif color == "c":
        my_stick.set_all_LED_color(0, 100, 100)
    elif color == "q":
        exit(0)
    else:
        pass

