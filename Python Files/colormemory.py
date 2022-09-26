import layout
from time import sleep
import random
from ws2812 import WS2812
import machine
import math
import json

memorizeCount = 2
startRound = 1
roundInc = 3

with open('JSONFiles/save.json', 'r') as f:
      saveJson = json.load(f)

highestScore = saveJson["memoryHighScore"]

previous_value = True
button_bounce = True

layout.oled.init_display()

power = machine.Pin(11,machine.Pin.OUT)
power.value(1)
layout.oled.init_display()

with open('JSONFiles/colors.json', 'r') as f:
  colors = json.load(f)
  
def jsonSave(key, value):
    saveJson = open("JSONFiles/save.json", "r")
    jsonObject = json.load(saveJson)
    saveJson.close()

    jsonObject[key] = value

    saveJson = open("JSONFiles/save.json", "w")
    json.dump(jsonObject, saveJson)
    saveJson.close()
    
def randomColor(color):
    led = WS2812(12,1)
    led.pixels_fill(colors[color])
    led.pixels_show()
    
def screen(page, all_pages):
    layout.oled.fill_rect(0,0,layout.width,layout.height,0)
    layout.oled.text(all_pages[page][0],1,1)
    layout.oled.text(all_pages[page][1],60,1)
    layout.oled.text(all_pages[page][2],1,11)
    layout.oled.text(all_pages[page][3],60,11)
    layout.oled.text(all_pages[page][4],1,21)
    layout.oled.text(all_pages[page][5],60,21)
    layout.oled.show()
        
def game(memorize, rounds):
    generColorList = []
    global highestScore
    
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
        layout.oled.text(displayText,1,21)
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
        elif layout.button23.value():
            if len(userColorList) > 0:
                userColorList.pop()
                dispUserList.pop()
                layout.oled.fill_rect(0,21,layout.width,layout.height,0)
                layout.oled.show()
            sleep(.5)
            
    if userColorList == generColorList:
        layout.oled.fill_rect(0,21,layout.width,layout.height,0)
        layout.oled.show()
        layout.oled.text("Correct",1,21)
        layout.oled.show()
        sleep(1)
        layout.oled.fill_rect(0,21,layout.width,layout.height,0)
        layout.oled.show()
        sleep(.5)
        rounds += 1
        layout.oled.text("Round: {}".format(rounds),1,21)
        layout.oled.show()
        sleep(1)
        layout.oled.fill_rect(0,21,layout.width,layout.height,0)
        layout.oled.show()
        sleep(.5)
        if (rounds % roundInc) == 0:
            memorize += 1
        game(memorize, rounds)

    else:
        layout.oled.fill_rect(0,0,layout.width,layout.height,0)
        layout.oled.show()
        layout.oled.text("Wrong",1,1)
        layout.oled.show()
        sleep(1)
        layout.oled.fill_rect(0,0,layout.width,layout.height,0)
        layout.oled.show()
        sleep(.5)
        layout.oled.text("Rounds Complete:",1,1)
        layout.oled.text(str(rounds-1),1,11)
        layout.oled.show()
        sleep(1)
        if (rounds-1) > highestScore:
            layout.oled.text("New Highscore",1,21)
            layout.oled.show()
            sleep(1)
            layout.oled.fill_rect(0,21,layout.width,layout.height,0)
            layout.oled.show()
            highestScore = rounds - 1
            jsonSave("memoryHighScore", highestScore)
        layout.oled.fill_rect(0,0,layout.width,layout.height,0)
        layout.oled.show()
        sleep(.5)    


# Modify the container name for an empty section
empty = ""
#List the macros
listKeys = ['Blue', 'Yellow', 'Green', 'Red']
randomColor("Off")
page = 0

# Finding the number of pages in a category
total_page = math.ceil(len(listKeys)/6)

# Seperating a category of macros into pages
count = 0
pageList = []
for i in range(total_page):
    nestList = []
    for j in range(6):
        if count < len(listKeys):
            nestList.append(listKeys[count])
        else:
            nestList.append(empty)
        count += 1
    pageList.append(nestList)

while button_bounce:
    layout.oled.text("Ready",1,1)
    layout.oled.text("Highscore: {}".format(highestScore),1,21)
    layout.oled.show()
    if layout.button11.value():
        screen(0, pageList)
        sleep(1)
        game(memorizeCount, startRound)
    
    if layout.button_pin.value() == False:
        layout.oled.fill_rect(0,0,layout.width,layout.height,0)
        layout.oled.text("Going Back", 1, 10)
        layout.oled.text("To Menu", 1, 21)
        layout.oled.show()
        sleep(1)
        button_bounce = False

