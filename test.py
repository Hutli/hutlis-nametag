#!/usr/bin/env python3

import argparse

from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from inky.auto import auto


print("""Inky pHAT/wHAT: Hello... my name is:

Use Inky pHAT/wHAT as a personalised name badge!

""")

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


# Create a new canvas to draw on

# img = Image.new("P", inky_display.resolution)
# draw = ImageDraw.Draw(img)

for x in range(50):
    for y in range(0, 50):
        inky_display.set_pixel(x, y, inky_display.WHITE)


# Load the fonts

# font = ImageFont.truetype(HankenGroteskBold, int(12))

# # Grab the name to be displayed

# name = args.name
# name_w, name_h = font.getsize(name)
# name_x = int((inky_display.width - name_w) / 2)
# name_y = int(y_top + ((y_bottom - y_top - name_h) / 2))
# draw.text((name_x, name_y), name, inky_display.BLACK, font=font)

# Display the completed name badge

inky_display.set_image(img)
inky_display.show()
