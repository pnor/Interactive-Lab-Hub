#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont

# from Typing import *
from datetime import datetime, timedelta
import adafruit_rgb_display.st7789 as st7789
import board
import digitalio
import os
import qwiic_button
import random
import subprocess
import subprocess
import sys
import time
import time
import typing
from colour import Color


cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
# ============================================================


def speak(words: str) -> None:
    os.popen(f'echo "{words}" | festival --tts')


def light_up(color: str) -> None:
    draw.rectangle((0, 0, width, height), outline=0, fill=(1, 0, 0))


if __name__ == "__main__":
    color_range = list(Color("#000000").range_to(Color("#ff0000"), 10))
    color_range = list(map(lambda c: c.hex, color_range))
    prog = 0

    while True:
        usr_input = input("=> ").strip()
        if usr_input == "l":
            prog += 1
            light_up(color_range[prog % len(color_range)])
            print(f"lighting to {color_range[prog % len(color_range)]}")
        elif usr_input == "end" or usr_input == 'q':
            break
        elif usr_input == "reset":
            prog = 0
            print("progress set to 0")
        elif usr_input == "":
            print("...")
            continue
        else:
            speak(usr_input)
            print(f"saying {usr_input}")
