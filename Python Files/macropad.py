# Author: SacredAntwon
# Purpose: Runs the main menu and option selection.

import layout
from ws2812 import WS2812
import machine
from time import sleep
import math
import re
import keycode
import json
from collections import OrderedDict

# Get the list of categories from macros.json and display the menu
with open('JSONFiles/macros.json', 'r') as f:
    macroJson = json.load(f)

# Convert to list
fileList = list(macroJson)
programFiles = ['Etch', 'RGB', 'Blackjack',  'Colormemory']
fileList += programFiles

# Main menu line constants
line = 1
highlight = 1
shift = 0
listLength = 0
totalLines = 3

# Initialize oled
layout.oled.init_display()

# Rotary encoder button
previousValue = True
buttonDown = False

# Function to set the color for the rgb led
def setColor():
    global colorCode
    # Get the save data for last set color
    with open('JSONFiles/save.json', 'r') as f:
        saveJson = json.load(f)

    # Get color codes
    with open('JSONFiles/colors.json', 'r') as f:
        colorsJson = json.load(f)

    power = machine.Pin(11, machine.Pin.OUT)
    power.value(1)
    layout.oled.init_display()

    selectedColor = saveJson["lastColor"]
    led = WS2812(12, 1)
    colorCode = colorsJson[selectedColor]
    led.pixels_fill(colorCode)
    led.pixels_show()


# Splits string and converts each element to keycode (Hex)
def convertKey(keyString):
    keyList = []
    itemList = []
    keyList = re.sub(r"([A-Z])", r" \1", keyString).split()
    for key in keyList:
        itemList.append(keycode.keys[key])
    return itemList

# Function for determining what type of macro to use
def macroType(listCateg, pageList, page, button):
    itemString = listCateg[pageList[page][button]]['keys']
    itemList = convertKey(itemString)
    itemType = listCateg[pageList[page][button]]['type']
    itemSleep = listCateg[pageList[page][button]]['wait']
    if itemType == 'separate':
        for item in itemList:
            layout.k.press(item)
            layout.k.release(item)
    elif itemType == 'together':
        for item in itemList:
            layout.k.press(item)
        for item in itemList:
            layout.k.release(item)
    elif itemType == 'control':
        layout.cc.send(itemList[0])

    # Modify in macros.py under "wait" key
    sleep(itemSleep)

# Function for displaying screen in a macro category
def screen(page, allPages):
    layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
    layout.oled.text(allPages[page][0], 1, 1)
    layout.oled.text(allPages[page][1], 60, 1)
    layout.oled.text(allPages[page][2], 1, 11)
    layout.oled.text(allPages[page][3], 60, 11)
    layout.oled.text(allPages[page][4], 1, 21)
    layout.oled.text(allPages[page][5], 60, 21)
    layout.oled.show()

# Function will run when a category is selected
def running(categ):
    previousVal = True
    buttonBoun = True

    listCateg = macroJson[categ]

    # Modify the container name for an empty section
    empty = ""
    # List the macros
    listKeys = list(listCateg.keys())

    page = 0

    # Finding the number of pages in a category
    totalPage = math.ceil(len(listKeys)/6)

    # Separating a category of macros into pages
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

    # Call screen function to display the macros
    screen(0, pageList)

    # This while loop will run until rotary encoder is clicked
    while buttonBoun:
        if previousVal != layout.stepPin.value():
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

            previousVal = layout.stepPin.value()

        # Top left button
        if layout.button11.value():
            if pageList[page][0] != empty:
                macroType(listCateg, pageList, page, 0)

        # Top right button
        elif layout.button21.value():
            if pageList[page][1] != empty:
                macroType(listCateg, pageList, page, 1)

        # Middle left button
        elif layout.button12.value():
            if pageList[page][2] != empty:
                macroType(listCateg, pageList, page, 2)

        # Middle right button
        elif layout.button22.value():
            if pageList[page][3] != empty:
                macroType(listCateg, pageList, page, 3)

        # Bottom left button
        elif layout.button13.value():
            if pageList[page][4] != empty:
                macroType(listCateg, pageList, page, 4)

        # Bottom right button
        elif layout.button23.value():
            if pageList[page][5] != empty:
                macroType(listCateg, pageList, page, 5)

        # Exits the loop and goes back to main function
        if layout.buttonPin.value() == False:
            layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
            layout.oled.text("Going Back", 1, 10)
            layout.oled.text("To Menu", 1, 21)
            layout.oled.show()
            sleep(1)
            buttonBoun = False


# Main menu for showing categories
def showMenu(menu):
    # Get globals
    global line, highlight, shift, listLength

    # Initialize variables
    item = 1
    line = 1
    lineHeight = 10

    # Clear display
    layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)

    # Shift the list of categories so that it shows on the display
    listLength = len(menu)
    shortList = menu[shift:shift+totalLines]

    for item in shortList:
        if highlight == line:
            layout.oled.fill_rect(0, (line-1)*lineHeight,
                                  layout.width, lineHeight, 1)
            layout.oled.text(">", 0, (line-1)*lineHeight, 0)
            layout.oled.text(item, 10, (line-1)*lineHeight, 0)
            layout.oled.show()
        else:
            layout.oled.text(item, 10, (line-1)*lineHeight, 1)
            layout.oled.show()
        line += 1
    layout.oled.show()

# Launching a file


def launch(filename):
    global fileList
    # Clear screen
    layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
    layout.oled.text("Launching", 1, 10)
    layout.oled.text(filename, 1, 20)
    layout.oled.show()
    sleep(2)
    if filename in programFiles:
        program(filename)
    else:
        running(filename)

    showMenu(fileList)

# Function for launching files


def program(filename):
    # Etch file
    if filename == 'Etch':
        layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
        layout.oled.text("Rotate", 1, 1)
        layout.oled.text("Invert", 60, 1)
        layout.oled.text("Clear", 1, 11)
        layout.oled.text("PC Draw", 60, 11)
        layout.oled.show()
        sleep(2)
        exec(open("etch.py").read())

    # Blackjack file
    elif filename == 'Blackjack':
        layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
        layout.oled.text("Hit", 1, 21)
        layout.oled.text("Stand", 60, 21)
        layout.oled.show()
        sleep(2)
        exec(open("blackjack.py").read())

    # Colormemory file
    elif filename == 'Colormemory':
        layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
        layout.oled.text("Confirm", 1, 21)
        layout.oled.text("Back", 65, 21)
        layout.oled.show()
        sleep(2)
        exec(open("colormemory.py").read())
        setColor()
        showMenu(fileList)

    # RGB file
    elif filename == 'RGB':
        exec(open("rgb.py").read())
        showMenu(fileList)


# Ensure correct color is set
setColor()

showMenu(fileList)

# Repeat forever
while True:
    # Control audio in main menu with top left button
    while layout.button11.value():
        if previousValue != layout.stepPin.value():
            if layout.stepPin.value() == False:

                # Turned Left
                if layout.directionPin.value() == False:
                    layout.cc.send(convertKey("Voldown")[0])

                # Turned Right
                else:
                    layout.cc.send(convertKey("Volup")[0])
            previousValue = layout.stepPin.value()

    # This will allow for testing of all buttons and display
    if layout.button12.value() and layout.button22.value():
        layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
        layout.oled.text("Test Device", 1, 10)
        layout.oled.show()
        sleep(1)
        exec(open("test.py").read())
        showMenu(fileList)

    # This will launch the selected category
    if previousValue != layout.stepPin.value():
        if layout.stepPin.value() == False:

            # Turned Left
            if layout.directionPin.value() == False:
                if highlight > 1:
                    highlight -= 1
                else:
                    if shift > 0:
                        shift -= 1

            # Turned Right
            else:
                if highlight < totalLines:
                    highlight += 1
                else:
                    if shift+totalLines < listLength:
                        shift += 1

            showMenu(fileList)
        previousValue = layout.stepPin.value()

    # Check for button pressed
    if layout.buttonPin.value() == False and not buttonDown:
        buttonDown = True

        # Goes to function for running a category
        launch(fileList[(highlight-1) + shift])

    # Decbounce button
    if layout.buttonPin.value() == True and buttonDown:
        buttonDown = False
