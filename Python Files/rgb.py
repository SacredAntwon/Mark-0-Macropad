from ws2812 import WS2812
import machine
from time import sleep
import layout
import math
import json

power = machine.Pin(11,machine.Pin.OUT)
power.value(1)
layout.oled.init_display()

with open('colors.json', 'r') as f:
  colors = json.load(f)
  
def jsonSave(key, value):
    saveJson = open("save.json", "r")
    jsonObject = json.load(saveJson)
    saveJson.close()

    jsonObject[key] = value

    saveJson = open("save.json", "w")
    json.dump(jsonObject, saveJson)
    saveJson.close()

def led(pageList, page, button):
    selectedColor = pageList[page][button]
    led = WS2812(12,1)
    led.pixels_fill(colors[selectedColor])
    led.pixels_show()
    jsonSave("lastColor", selectedColor)
    
def screen(page, all_pages):
    layout.oled.fill_rect(0,0,layout.width,layout.height,0)
    layout.oled.text(all_pages[page][0],1,1)
    layout.oled.text(all_pages[page][1],60,1)
    layout.oled.text(all_pages[page][2],1,11)
    layout.oled.text(all_pages[page][3],60,11)
    layout.oled.text(all_pages[page][4],1,21)
    layout.oled.text(all_pages[page][5],60,21)
    layout.oled.show()

previous_value = True
button_bounce = True

# Modify the container name for an empty section
empty = ""
#List the macros
listKeys = list(colors.keys())
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

screen(0, pageList)

while button_bounce:
    if previous_value != layout.step_pin.value():
        if layout.step_pin.value() == False:

            # Turned Left
            if layout.direction_pin.value() == False:
                if page > 0:
                    page -= 1

            # Turned Right
            else:
                if page < total_page - 1:
                    page += 1
            
            screen(page, pageList)

        previous_value = layout.step_pin.value()
        
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
        
    if layout.button_pin.value() == False:
        layout.oled.fill_rect(0,0,layout.width,layout.height,0)
        layout.oled.text("Going Back", 1, 10)
        layout.oled.text("To Menu", 1, 21)
        layout.oled.show()
        sleep(1)
        button_bounce = False

