import board
import random
import digitalio
import subprocess
import time
from datetime import datetime, timedelta
import typing
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from colour import Color

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
color_off: str = "#000000"
color_on: str = "#00ffff"
cur_color: str = "#00ffff"
target_color: str = "#ff00ff"
text_color: str = "#ffffff"


# ===== Helper Functions for drawing to the screen =====
Rectangle = tuple[float, float, float, float]
RectangleColorPair = tuple[Rectangle, str]


def hour_rectangles(hour: int) -> list[Rectangle]:
    return rectangles_for_number(hour)


def minute_rectangles(minute: int) -> list[Rectangle]:
    shift_amount = width / 3
    rects = map(lambda r: shift_right(r, shift_amount), rectangles_for_number(minute))
    return list(rects)


def second_rectangles(second: int) -> list[Rectangle]:
    shift_amount = (2 * width) / 3
    rects = map(lambda r: shift_right(r, shift_amount), rectangles_for_number(second))
    return list(rects)


def rectangles_for_number(number: int) -> list[Rectangle]:
    assert number < 100
    assert number >= 0

    rectangles: list[Rectangle] = []
    rectangle_width = (width / 3) / 2
    rectangle_height = height / 4
    base_rect = [0, 0, rectangle_width, rectangle_height]

    # 10s
    left_digit = int(number / 10)
    if left_digit >= 8:
        left_digit -= 8
        rectangles += [base_rect]
    if left_digit >= 4:
        left_digit -= 4
        rectangles += [shift_down(base_rect, rectangle_height)]
    if left_digit >= 2:
        left_digit -= 2
        rectangles += [shift_down(base_rect, rectangle_height * 2)]
    if left_digit >= 1:
        left_digit -= 1
        rectangles += [shift_down(base_rect, rectangle_height * 3)]
    # 1s
    right_digit = int(number % 10)
    if right_digit >= 8:
        right_digit -= 8
        rectangles += [shift_right(base_rect, rectangle_width)]
    if right_digit >= 4:
        right_digit -= 4
        rectangles += [
            shift_right(shift_down(base_rect, rectangle_height), rectangle_width)
        ]
    if right_digit >= 2:
        right_digit -= 2
        rectangles += [
            shift_right(shift_down(base_rect, rectangle_height * 2), rectangle_width)
        ]
    if right_digit >= 1:
        right_digit -= 1
        rectangles += [
            shift_right(shift_down(base_rect, rectangle_height * 3), rectangle_width)
        ]
    # return the results
    return rectangles


def shift_right(rect: Rectangle, amount) -> Rectangle:
    left, bot, right, top = rect
    return [left + amount, bot, right + amount, top]


def shift_down(rect: Rectangle, amount) -> Rectangle:
    left, bot, right, top = rect
    return [left, bot + amount, right, top + amount]


def calculate_rectangle_color_pairs(
    start: list[Rectangle], end: list[Rectangle], progress: float
) -> list[RectangleColorPair]:
    """Figure out the lerping from start to end rectangles"""
    # TODO: lotta work, mainly have to do some color arithmetic and convert it backh
    assert progress >= 0 and progress <= 1
    both: list[Rectangle | None] = map(
        lambda r: r if rect_equal_any(r, end) else None, start
    )
    both: list[Rectangle] = [b for b in both if b is not None]
    start = [s for s in start if not rect_equal_any(s, both)]
    end = [e for e in end if not rect_equal_any(e, both)]

    pairs: list[RectangleColorPair] = []
    pairs += [(r, color_on) for r in both]
    pairs += [(r, lerp_colors(color_off, color_on, (1 - progress))) for r in start]
    pairs += [(r, lerp_colors(color_off, color_on, progress)) for r in end]
    return pairs


def lerp_colors(start: str, end: str, progress: float) -> str:
    colors = list(Color(start).range_to(Color(end), 100))
    return colors[int(progress * len(colors))].hex


def rect_equal_any(r: Rectangle, others: list[Rectangle]) -> bool:
    filtered = filter(lambda o: rect_equal(r, o), others)
    return len(list(filtered)) > 0


def rect_equal(a: Rectangle, b: Rectangle) -> bool:
    aleft, atop, aright, abot = a
    bleft, btop, bright, bbot = b
    return (
        float_equal(aleft, bleft)
        and float_equal(atop, btop)
        and float_equal(aright, bright)
        and float_equal(abot, bbot)
    )


def float_equal(a: float, b: float) -> bool:
    tolerance = 0.01
    return abs(a - b) < tolerance


def draw_rectangles(rectangle_color_pairs: list[tuple[Rectangle, str]]):
    for pair in rectangle_color_pairs:
        rect, color = pair
        draw.rectangle(rect, outline=0, fill=color)


# ===== Helper Functions for working with the time
HoursMinutesSecondsMicro = list[int, int, int, int]

# ===== Drawing text labels
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)


def draw_labels(width: int, height: int):
    # digit significance
    for i in range(0, 6):
        draw.text(
            ((width / 12) + (i * (width / 6)), 5),
            text=("10" if i % 2 == 0 else "1"),
            font=font,
            fill=text_color,
        )
    # binary values
    for i in range(0, 4):
        draw.text(
            (5, height - (height / 8) - (i * (height / 4))),
            text=str(2**i),
            font=font,
            fill=text_color,
        )


def get_time_in_pieces(offset: int = 0) -> HoursMinutesSecondsMicro:
    t = datetime.now() + timedelta(seconds=offset)
    time_pieces = t.strftime("%H:%M:%S:%f").split(":")
    return list(map(lambda s: int(s), time_pieces))


def assign_colors_to_rects(
    now_time: list[Rectangle], next_time: list[Rectangle]
) -> RectangleColorPair:
    pass


COLOR_DURATION = 2
color_timer = 0
DELTA_TIME = 0.017
while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # =============
    # binary clock
    hours, minutes, secs, micro = get_time_in_pieces()
    rects = hour_rectangles(hours)
    rects += minute_rectangles(minutes)
    rects += second_rectangles(secs)
    next_hours, next_minutes, next_secs, next_micro = get_time_in_pieces(1)
    next_rects = hour_rectangles(next_hours)
    next_rects += minute_rectangles(next_minutes)
    next_rects += second_rectangles(next_secs)

    rect_pairs = calculate_rectangle_color_pairs(rects, next_rects, micro / 1000000)

    draw_rectangles(rect_pairs)
    draw_labels(width, height)

    # Make color change over time
    color_timer += DELTA_TIME
    color_on = lerp_colors(
        cur_color, target_color, min(0.9999, color_timer / COLOR_DURATION)
    )
    if color_timer >= COLOR_DURATION:
        color_timer = 0
        cur_color = Color(target_color).hex
        target_color = Color(hue=random.random(), saturation=1, luminance=0.5).hex

    # Display image.
    disp.image(image, rotation)
    time.sleep(DELTA_TIME)
