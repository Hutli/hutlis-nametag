#!/usr/bin/env python3

import argparse
import numpy
import struct
import time

from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from inky.auto import auto


def custom_update(inky_display, buf, busy_wait=True):
    buf = numpy.packbits(numpy.where(buf == inky_display.BLACK, 0, 1)).tolist()
    inky_display.setup()

    packed_height = list(struct.pack('<H', inky_display.rows))

    if isinstance(packed_height[0], str):
        packed_height = map(ord, packed_height)

    inky_display._send_command(0x74, 0x54)  # Set Analog Block Control
    inky_display._send_command(0x7e, 0x3b)  # Set Digital Block Control

    inky_display._send_command(0x01, packed_height + [0x00])  # Gate setting

    inky_display._send_command(0x03, 0x17)  # Gate Driving Voltage
    # Source Driving Voltage
    inky_display._send_command(0x04, [0x41, 0xAC, 0x32])

    inky_display._send_command(0x3a, 0x07)  # Dummy line period
    inky_display._send_command(0x3b, 0x04)  # Gate line width
    # Data entry mode setting 0x03 = X/Y increment
    inky_display._send_command(0x11, 0x03)

    inky_display._send_command(0x2c, 0x3c)  # VCOM Register, 0x3c = -1.5v?

    inky_display._send_command(0x3c, 0b00000000)
    if inky_display.border_colour == inky_display.BLACK:
        # GS Transition Define A + VSS + LUT0
        inky_display._send_command(0x3c, 0b00000000)
    elif inky_display.border_colour == inky_display.RED and inky_display.colour == 'red':
        # Fix Level Define A + VSH2 + LUT3
        inky_display._send_command(0x3c, 0b01110011)
    elif inky_display.border_colour == inky_display.YELLOW and inky_display.colour == 'yellow':
        # GS Transition Define A + VSH2 + LUT3
        inky_display._send_command(0x3c, 0b00110011)
    elif inky_display.border_colour == inky_display.WHITE:
        # GS Transition Define A + VSH2 + LUT1
        inky_display._send_command(0x3c, 0b00110001)

    if inky_display.colour == 'yellow':
        # Set voltage of VSH and VSL
        inky_display._send_command(0x04, [0x07, 0xAC, 0x32])
    if inky_display.colour == 'red' and inky_display.resolution == (400, 300):
        inky_display._send_command(0x04, [0x30, 0xAC, 0x22])

    inky_display._send_command(
        0x32, inky_display._luts[inky_display.lut])  # Set LUTs

    x_offset = 0x00
    x_end = 212
    y_offset = 0x05

    ram_x = [0x00, y_offset]
    ram_y = [0x00, 0x00, x_end, 0x00]

    print(f'RAM X Start/End: {ram_x}')
    print(f'RAM Y Start/End: {ram_y}')
    # Set RAM X Start/End
    inky_display._send_command(0x44, ram_x)
    # Set RAM Y Start/End
    inky_display._send_command(0x45, ram_y)

    # 0x24 == RAM B/W, 0x26 == RAM Red/Yellow/etc
    inky_display._send_command(0x4e, 0x00)  # Set RAM X Pointer Start
    # Set RAM Y Pointer Start
    inky_display._send_command(0x4f, [x_offset, 0x00])
    inky_display._send_command(0x24, buf)  # Set B/W Buffer

    inky_display._send_command(0x22, 0xC7)  # Display Update Sequence
    inky_display._send_command(0x20)  # Trigger Display Update
    time.sleep(0.05)

    if busy_wait:
        inky_display._busy_wait()
        inky_display._send_command(0x10, 0x01)  # Enter Deep Sleep


try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")

parser = argparse.ArgumentParser()
parser.add_argument('--name', '-n', type=str, required=True, help="Your name")
args, _ = parser.parse_known_args()

# inky_display.set_rotation(180)
try:
    inky_display.set_border(inky_display.RED)
except NotImplementedError:
    pass

# Figure out scaling for display size

scale_size = 1.0
padding = 0

if inky_display.resolution == (400, 300):
    scale_size = 2.20
    padding = 15

if inky_display.resolution == (600, 448):
    scale_size = 2.20
    padding = 30

if inky_display.resolution == (250, 122):
    scale_size = 1.30
    padding = -5

# Create a new canvas to draw on

img = Image.new("P", inky_display.resolution)
# draw = ImageDraw.Draw(img)

# # Load the fonts

# intuitive_font = ImageFont.truetype(Intuitive, int(22 * scale_size))
# hanken_bold_font = ImageFont.truetype(HankenGroteskBold, int(35 * scale_size))
# hanken_medium_font = ImageFont.truetype(
#     HankenGroteskMedium, int(16 * scale_size))

# # Grab the name to be displayed

# name = args.name

# # Top and bottom y-coordinates for the white strip

# y_top = int(inky_display.height * (5.0 / 10.0))
# y_bottom = y_top + int(inky_display.height * (4.0 / 10.0))

# # Draw the red, white, and red strips

# for y in range(0, y_top):
#     for x in range(0, inky_display.width):
#         img.putpixel((x, y), inky_display.BLACK if inky_display.colour ==
#                      "black" else inky_display.RED)

# for y in range(y_top, y_bottom):
#     for x in range(0, inky_display.width):
#         img.putpixel((x, y), inky_display.WHITE)

# for y in range(y_bottom, inky_display.height):
#     for x in range(0, inky_display.width):
#         img.putpixel((x, y), inky_display.BLACK if inky_display.colour ==
#                      "black" else inky_display.RED)

# # Calculate the positioning and draw the "Hello" text

# hello_w, hello_h = hanken_bold_font.getsize("Hello")
# hello_x = int((inky_display.width - hello_w) / 2)
# hello_y = 0 + padding
# draw.text((hello_x, hello_y), "Hello",
#           inky_display.WHITE, font=hanken_bold_font)

# # Calculate the positioning and draw the "my name is" text

# mynameis_w, mynameis_h = hanken_medium_font.getsize("my name is")
# mynameis_x = int((inky_display.width - mynameis_w) / 2)
# mynameis_y = hello_h + padding
# draw.text((mynameis_x, mynameis_y), "my name is",
#           inky_display.WHITE, font=hanken_medium_font)

# # Calculate the positioning and draw the name text

# name_w, name_h = intuitive_font.getsize(name)
# name_x = int((inky_display.width - name_w) / 2)
# name_y = int(y_top + ((y_bottom - y_top - name_h) / 2))
# draw.text((name_x, name_y), name, inky_display.BLACK, font=intuitive_font)

# Display the completed name badge

inky_display.set_image(img)
inky_display.show()

print("Setting pixels")

width = inky_display.width
height = int(inky_display.height / 2)

buf = numpy.zeros((width, height), dtype=numpy.uint8)

for x in range(width):
    for y in range(height):
        buf[x][y] = inky_display.BLACK

custom_update(inky_display, buf)
