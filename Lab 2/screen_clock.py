import board
import digitalio
import subprocess
import time
import typing
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
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

# Setup constants and related
# Buttons
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()
# Colors
colorOff = "#000000"
colorOn = "#00ffff"


# ===== Helper Functions for drawing to the screen =====
Rectangle = tuple[float, float, float, float]
RectangleColorPair = tuple[rectangle, str]


def hour_rectangles(hour: int) -> list[Rectangle]:
    pass


def minute_rectangles(minute: int) -> list[Rectangle]:
    pass


def second_rectangles(second: int) -> list[Rectangle]:
    pass


def calculate_rectangle_color_pairs(
    startRects: list[Rectangle], endRects: list[Rectangle], progress: float
) -> RectangleColorPair:
    """Figure out the lerping from start to end rectangles"""
    pass


def draw_rectangles(rectangleColorPairs: tuple[Rectangle, str]):
    pass


# ===== Helper Functions for working with the time
HoursMinutesSecondsMicro = [int, int, int, int]


def getTimeInPieces() -> HoursMinutesSecondsMicro:
    pass


while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # =============
    # binary clock

    if buttonA.value:
        colorEven = "#ff00ff"
    else:
        colorEven = "#ff0000"

    cur_time = time.time()
    print(cur_time)
    if int(cur_time) % 2 == 0:
        print("a")
        draw.rectangle((0, 0, width, height), outline=0, fill=colorEven)
    else:
        print("b")
        draw.rectangle((0, 0, width, height), outline=0, fill=colorOdd)
        # a change to deploy?

    # Display image.
    disp.image(image, rotation)
    time.sleep(0.5)
