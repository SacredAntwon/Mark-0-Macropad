# Author: SacredAntwon
# Purpose: Allows users to select a color for
# the RGB Led.

from ws2812 import WS2812
import machine
from time import sleep
import layout
import math
import json

# Initialize pins for led
power = machine.Pin(11, machine.Pin.OUT)
power.value(1)
layout.oled.init_display()

# Load colors file from colors.json
with open('JSONFiles/colors.json', 'r') as f:
    colors = json.load(f)

# Function for writing to save.json
def jsonSave(key, value):
    saveJson = open("JSONFiles/save.json", "r")
    jsonObject = json.load(saveJson)
    saveJson.close()

    jsonObject[key] = value

    saveJson = open("JSONFiles/save.json", "w")
    json.dump(jsonObject, saveJson)
    saveJson.close()

# Function to display and save color
def led(pageList, page, button):
    selectedColor = pageList[page][button]
    led = WS2812(12, 1, 1)
    led.pixels_fill(colors[selectedColor])
    led.pixels_show()
    jsonSave("lastColor", selectedColor)

# Function for displaying elements
def screen(page, allPages):
    layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
    layout.oled.text(allPages[page][0], 1, 1)
    layout.oled.text(allPages[page][1], 60, 1)
    layout.oled.text(allPages[page][2], 1, 11)
    layout.oled.text(allPages[page][3], 60, 11)
    layout.oled.text(allPages[page][4], 1, 21)
    layout.oled.text(allPages[page][5], 60, 21)
    layout.oled.show()


previousValue = True
buttonBounce = True

# Modify the container name for an empty section
empty = ""
# List the macros
listKeys = list(colors.keys())
page = 0

# Finding the number of pages in a category
totalPage = math.ceil(len(listKeys)/6)

# Seperating a category of macros into pages
count = 0
pageList = []
for i in range(totalPage):
    nestList = []
    for j in range(6):
        if count < len(listKeys):
            nestList.append(listKeys[count])
        else:
            nestList.append(empty)
        count += 1
    pageList.append(nestList)

screen(0, pageList)

while buttonBounce:
    if previousValue != layout.stepPin.value():
        if layout.stepPin.value() == False:

            # Turned Left
            if layout.directionPin.value() == False:
                if page > 0:
                    page -= 1

            # Turned Right
            else:
                if page < totalPage - 1:
                    page += 1

            screen(page, pageList)

        previousValue = layout.stepPin.value()

    if layout.button11.value():
        if pageList[page][0] != empty:
            led(pageList, page, 0)
        sleep(.5)
    elif layout.button21.value():
        if pageList[page][1] != empty:
            led(pageList, page, 1)
        sleep(.5)
    elif layout.button12.value():
        if pageList[page][2] != empty:
            led(pageList, page, 2)
        sleep(.5)
    elif layout.button22.value():
        if pageList[page][3] != empty:
            led(pageList, page, 3)
        sleep(.5)
    elif layout.button13.value():
        if pageList[page][4] != empty:
            led(pageList, page, 4)
        sleep(.5)
    elif layout.button23.value():
        if pageList[page][5] != empty:
            led(pageList, page, 5)
        sleep(.5)

    # Go back to main menu
    if layout.buttonPin.value() == False:
        layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
        layout.oled.text("Going Back", 1, 10)
        layout.oled.text("To Menu", 1, 21)
        layout.oled.show()
        sleep(1)
        buttonBounce = False
