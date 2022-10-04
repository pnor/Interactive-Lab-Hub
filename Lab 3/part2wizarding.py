#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
from Typing import *
from datetime import datetime, timedelta
import adafruit_rgb_display.st7789 as st7789
import board
import digitalio
import os
import qwiic_button
import random
import subprocess
import sys
import time
import time
import typing
from colour import Color


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
# setting up drawing
BAUDRATE = 64000000
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

# ============================================================


def setup_screen() -> None:
    pass


def speak(words: str) -> None:
    os.popen(f'echo "{words}" | festival --tts')


def light_up(color: str) -> None:
    draw.rectangle((0, 0, width, height), outline=0, fill=color)


if __name__ == "__main__":
    color_range = list(Color("#000000").range_to(Color("#ff0000"), 100))
    color_range: List[str] = list(map(lambda c: c.hex, color_range))
    prog = 0

    while True:
        usr_input = input("=> ")
        if usr_input == "l":
            prog += 1
            light_up(color_range[prog % len(color_range)])
        elif usr_input == "end":
            speak(usr_input)
        else:
            break
