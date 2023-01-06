# Author: SacredAntwon
# Purpose: This file is for testing purposes.
# Test if your device works correctly with this.
# Access this menu by pressing the middle left and
# middle right buttons at the same time.

from time import sleep
import layout

# Test lists
pageOne = ["A", "B", "C", "D", "E", "F"]
pageTwo = ["1", "2", "3", "4", "5", "6"]
allPages = [pageOne, pageTwo]

# Initialize display
layout.oled.init_display()

# Function for displaying elements
def screen(page):
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

# Initialize variables
page = 0
totalPage = 1

screen(0)

while buttonBounce:
    if previousValue != layout.stepPin.value():
        if layout.stepPin.value() == False:

            # Turned Left
            if layout.directionPin.value() == False:
                if page > 0:
                    page -= 1

            # Turned Right
            else:
                if page < totalPage:
                    page += 1

            screen(page)
            sleep(.5)

        previousValue = layout.stepPin.value()

    layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
    layout.oled.show()

    while layout.button11.value():
        if page == 0:
            layout.k.press(0x04)
            layout.k.release(0x04)
        elif page == 1:
            layout.k.press(0x1e)
            layout.k.release(0x1e)
        layout.oled.text(allPages[page][0], 1, 1)
        layout.oled.show()
        sleep(.1)

    while layout.button21.value():
        if page == 0:
            layout.k.press(0x05)
            layout.k.release(0x05)
        elif page == 1:
            layout.k.press(0x1f)
            layout.k.release(0x1f)
        layout.oled.text(allPages[page][1], 60, 1)
        layout.oled.show()
        sleep(.1)

    while layout.button12.value():
        if page == 0:
            layout.k.press(0x06)
            layout.k.release(0x06)
        elif page == 1:
            layout.k.press(0x20)
            layout.k.release(0x20)
        layout.oled.text(allPages[page][2], 1, 11)
        layout.oled.show()
        sleep(.1)

    while layout.button22.value():
        if page == 0:
            layout.k.press(0x07)
            layout.k.release(0x07)
        elif page == 1:
            layout.k.press(0x21)
            layout.k.release(0x21)
        layout.oled.text(allPages[page][3], 60, 11)
        layout.oled.show()
        sleep(.1)

    while layout.button13.value():
        if page == 0:
            layout.k.press(0x08)
            layout.k.release(0x08)
        elif page == 1:
            layout.k.press(0x22)
            layout.k.release(0x22)
        layout.oled.text(allPages[page][4], 1, 21)
        layout.oled.show()
        sleep(.1)

    while layout.button23.value():
        if page == 0:
            layout.k.press(0x09)
            layout.k.release(0x09)
        elif page == 1:
            layout.k.press(0x23)
            layout.k.release(0x23)
        layout.oled.text(allPages[page][5], 60, 21)
        layout.oled.show()
        sleep(.1)

    if layout.buttonPin.value() == False:
        layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
        layout.oled.text("Going Back", 1, 10)
        layout.oled.text("To Menu", 1, 21)
        layout.oled.show()
        sleep(1)
        buttonBounce = False
