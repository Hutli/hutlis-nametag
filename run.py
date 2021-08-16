#!/usr/bin/env python3

import argparse

from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from inky import InkyPHAT
from fastapi import FastAPI, Response, status
from fastapi.responses import PlainTextResponse, HTMLResponse


app = FastAPI()

try:
    inky_display = InkyPHAT('red')
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")

# inky_display.set_rotation(180)
try:
    inky_display.set_border(inky_display.RED)
except NotImplementedError:
    pass

# Create a new canvas to draw on
img = Image.new("P", inky_display.resolution)
draw = ImageDraw.Draw(img)

# Load the fonts
intuitive_font = ImageFont.truetype(Intuitive, 30)
hanken_bold_font = ImageFont.truetype(HankenGroteskBold, 35)
hanken_medium_font = ImageFont.truetype(HankenGroteskMedium, 16)

# Top and bottom y-coordinates for the white strip
y_top = int(inky_display.height * (5.0 / 10.0))
y_bottom = y_top + int(inky_display.height * (4.0 / 10.0))

# Draw the red, white, and red strips
for y in range(0, y_top):
    for x in range(0, inky_display.width):
        img.putpixel((x, y), inky_display.BLACK if inky_display.colour ==
                     "black" else inky_display.RED)

for y in range(y_top, y_bottom):
    for x in range(0, inky_display.width):
        img.putpixel((x, y), inky_display.WHITE)

for y in range(y_bottom, inky_display.height):
    for x in range(0, inky_display.width):
        img.putpixel((x, y), inky_display.BLACK if inky_display.colour ==
                     "black" else inky_display.RED)


# Calculate the positioning and draw the "Hello" text
hello_w, hello_h = hanken_bold_font.getsize("Hello")
hello_x = int((inky_display.width - hello_w) / 2)
hello_y = 0
draw.text((hello_x, hello_y), "Hello",
          inky_display.WHITE, font=hanken_bold_font)

# Calculate the positioning and draw the "my name is" text
mynameis_w, mynameis_h = hanken_medium_font.getsize("my name is")
mynameis_x = int((inky_display.width - mynameis_w) / 2)
mynameis_y = hello_h
draw.text((mynameis_x, mynameis_y), "my name is",
          inky_display.WHITE, font=hanken_medium_font)


inky_display.set_image(img)
inky_display.show()


@app.get("/nametag/{name}", status_code=200)
def read_item(name: str):
    for y in range(y_top, y_bottom):
        for x in range(0, inky_display.width):
            img.putpixel((x, y), inky_display.WHITE)

    # Calculate the positioning and draw the name text
    name_w, name_h = intuitive_font.getsize(name)
    name_x = int((inky_display.width - name_w) / 2)
    name_y = int(y_top + ((y_bottom - y_top - name_h) / 2))
    draw.text((name_x, name_y), name, inky_display.BLACK, font=intuitive_font)

    # Display the completed name badge
    inky_display.set_image(img)
    inky_display.show()

    return "Done!"
