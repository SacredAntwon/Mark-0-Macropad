# Author: Anthony Maida
# Purpose: Game to memorize colors in a
# random order.

import layout
from time import sleep
from ws2812 import WS2812
import random
import machine
import math
import json

# Clear screen
layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
layout.oled.show()

# Initializing variables
memorizeCount = 1
startRound = 1
roundInc = 1

# Get save information from save.json
with open('JSONFiles/save.json', 'r') as f:
    saveJson = json.load(f)

highestScore = saveJson["memoryHighScore"]

previousValue = True
buttonBounce = True

# Get LED
led = WS2812(12, 1, 1)

# Get all color codes from colors.json
with open('JSONFiles/colors.json', 'r') as f:
    colors = json.load(f)

# Function for saving information
def jsonSave(key, value):
    saveJson = open("JSONFiles/save.json", "r")
    jsonObject = json.load(saveJson)
    saveJson.close()

    jsonObject[key] = value

    saveJson = open("JSONFiles/save.json", "w")
    json.dump(jsonObject, saveJson)
    saveJson.close()

# Function for showing color
def randomColor(color):
    led.pixels_fill(colors[color])
    led.pixels_show()

# Function for screen
def screen(page, allPages):
    layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
    layout.oled.text(allPages[page][0], 1, 1)
    layout.oled.text(allPages[page][1], 60, 1)
    layout.oled.text(allPages[page][2], 1, 11)
    layout.oled.text(allPages[page][3], 60, 11)
    layout.oled.text(allPages[page][4], 1, 21)
    layout.oled.text(allPages[page][5], 60, 21)
    layout.oled.show()

# Main game function
def game(memorize, rounds):
    generColorList = []
    global highestScore

    # Will go through and display colors depending on the round
    for num in range(memorize):
        randColorInt = random.randint(0, len(listKeys)-1)
        randomColor(listKeys[randColorInt])
        generColorList.append(listKeys[randColorInt])
        sleep(1)
        randomColor("Off")
        sleep(.5)

    dispUserList = []
    userColorList = []

    while layout.button13.value() == False:
        displayText = ''.join(dispUserList)
        layout.oled.text(displayText, 1, 21)
        layout.oled.show()

        if layout.button11.value():
            userColorList.append(listKeys[0])
            dispUserList.append(listKeys[0][0])
            sleep(.5)
        elif layout.button21.value():
            userColorList.append(listKeys[1])
            dispUserList.append(listKeys[1][0])
            sleep(.5)
        elif layout.button12.value():
            userColorList.append(listKeys[2])
            dispUserList.append(listKeys[2][0])
            sleep(.5)
        elif layout.button22.value():
            userColorList.append(listKeys[3])
            dispUserList.append(listKeys[3][0])
            sleep(.5)

        # Backspace
        elif layout.button23.value():
            if len(userColorList) > 0:
                userColorList.pop()
                dispUserList.pop()
                layout.oled.fill_rect(0, 21, layout.width, layout.height, 0)
                layout.oled.show()
            sleep(.5)

    # Goes through if a correct selection is made
    if userColorList == generColorList:
        layout.oled.fill_rect(0, 21, layout.width, layout.height, 0)
        layout.oled.show()
        layout.oled.text("Correct", 1, 21)
        layout.oled.show()
        sleep(1)
        layout.oled.fill_rect(0, 21, layout.width, layout.height, 0)
        layout.oled.show()
        sleep(.5)
        rounds += 1
        layout.oled.text("Round: {}".format(rounds), 1, 21)
        layout.oled.show()
        sleep(1)
        layout.oled.fill_rect(0, 21, layout.width, layout.height, 0)
        layout.oled.show()
        sleep(.5)
        if (rounds % roundInc) == 0:
            memorize += 1
        game(memorize, rounds)

    # Goes through if a wrong selection is made
    else:
        layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
        layout.oled.show()
        layout.oled.text("Wrong", 1, 1)
        layout.oled.show()
        sleep(1)
        layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
        layout.oled.show()
        sleep(.5)
        layout.oled.text("Rounds Complete:", 1, 1)
        layout.oled.text(str(rounds-1), 1, 11)
        layout.oled.show()
        sleep(1)
        # Set new high score if one is achieved
        if (rounds-1) > highestScore:
            layout.oled.text("New Highscore", 1, 21)
            layout.oled.show()
            sleep(1)
            layout.oled.fill_rect(0, 21, layout.width, layout.height, 0)
            layout.oled.show()
            highestScore = rounds - 1
            jsonSave("memoryHighScore", highestScore)
        layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
        layout.oled.show()
        sleep(.5)


# Modify the container name for an empty section
empty = ""

# List the macros
listKeys = ['Blue', 'Yellow', 'Green', 'Red']
randomColor("Off")
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

while buttonBounce:
    layout.oled.text("Ready", 1, 1)
    layout.oled.text(f"Highscore: {highestScore}", 1, 21)
    layout.oled.show()
    if layout.button11.value():
        screen(0, pageList)
        sleep(1)
        game(memorizeCount, startRound)

    if layout.buttonPin.value() == False:
        layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
        layout.oled.text("Going Back", 1, 10)
        layout.oled.text("To Menu", 1, 21)
        layout.oled.show()
        sleep(1)
        buttonBounce = False
