import layout
from time import sleep
import math
import macros as m
import re
import keycode

# Get the list of categories from macro.py and display the menu
file_list = list(m.macros)

# Main menu line constants
line = 1
highlight = 1
shift = 0
list_length = 0
total_lines = 3

# Initialize oled
layout.oled.init_display()

# Rotary encoder button
previous_value = True
button_down = False

# Splits string and converts each element to keycode (Hex)
def convertKey(keyString):
    keyList = []
    itemList = []
    keyList = re.sub( r"([A-Z])", r" \1", keyString).split()
    for key in keyList:
        itemList.append(keycode.keys[key])

    return itemList

# Function for determining what type of macro to use
def macroType(listCateg, pageList, page, button):
    itemString = listCateg[pageList[page][button]]['keys']
    itemList = convertKey(itemString)
    itemType = listCateg[pageList[page][button]]['type']
    itemSleep = listCateg[pageList[page][button]]['wait']
    if itemType == 'seperate':
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
def screen(page, all_pages):
    layout.oled.fill_rect(0,0,layout.width,layout.height,0)
    layout.oled.text(all_pages[page][0],1,1)
    layout.oled.text(all_pages[page][1],60,1)
    layout.oled.text(all_pages[page][2],1,11)
    layout.oled.text(all_pages[page][3],60,11)
    layout.oled.text(all_pages[page][4],1,21)
    layout.oled.text(all_pages[page][5],60,21)
    layout.oled.show()

# This function will run when a category is selected
def running(categ):
    previous_val = True
    button_boun = True

    listCateg = m.macros[categ]

    # Modify the container name for an empty section
    empty = ""
    #List the macros
    listKeys = list(listCateg.keys())
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

    # Call screen function to display the macros
    screen(0, pageList)

    # This while loop will run until rotary encoder is clicked
    while button_boun:
        if previous_val != layout.step_pin.value():
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

            previous_val = layout.step_pin.value()

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
        if layout.button_pin.value() == False:
            layout.oled.fill_rect(0,0,layout.width,layout.height,0)
            layout.oled.text("Going Back", 1, 10)
            layout.oled.text("To Menu", 1, 21)
            layout.oled.show()
            sleep(1)
            button_boun = False


# Main menu for showing categories
def show_menu(menu):
    """ Shows the menu on the screen"""

    # bring in the global variables
    global line, highlight, shift, list_length

    # menu variables
    item = 1
    line = 1
    line_height = 10

    # clear the display
    layout.oled.fill_rect(0,0,layout.width,layout.height,0)

    # Shift the list of categories so that it shows on the display
    list_length = len(menu)
    short_list = menu[shift:shift+total_lines]

    for item in short_list:
        if highlight == line:
            layout.oled.fill_rect(0,(line-1)*line_height, layout.width,line_height,1)
            layout.oled.text(">",0, (line-1)*line_height,0)
            layout.oled.text(item, 10, (line-1)*line_height,0)
            layout.oled.show()
        else:
            layout.oled.text(item, 10, (line-1)*line_height,1)
            layout.oled.show()
        line += 1
    layout.oled.show()


def launch(filename):
    global file_list
    # clear the screen
    layout.oled.fill_rect(0,0,layout.width,layout.height,0)
    layout.oled.text("Launching", 1, 10)
    layout.oled.text(filename,1, 20)
    layout.oled.show()
    sleep(2)
    running(filename)
    show_menu(file_list)

show_menu(file_list)

# Repeat forever
while True:
    # This will display buttons and launch etch
    if layout.button11.value() and layout.button21.value():
        layout.oled.fill_rect(0,0,layout.width,layout.height,0)
        layout.oled.text("Etch", 1, 10)
        layout.oled.show()
        sleep(1)
        layout.oled.fill_rect(0,0,layout.width,layout.height,0)
        layout.oled.text("Rotate",1,1)
        layout.oled.text("Invert",60,1)
        layout.oled.text("Clear",1,11)
        layout.oled.text("PC Draw",60,11)
        layout.oled.show()
        sleep(2)
        exec(open("etch.py").read())
        show_menu(file_list)

    # This will display buttons and launch blackjack
    if layout.button12.value() and layout.button22.value():
        layout.oled.fill_rect(0,0,layout.width,layout.height,0)
        layout.oled.text("Blackjack", 1, 10)
        layout.oled.show()
        sleep(1)
        layout.oled.fill_rect(0,0,layout.width,layout.height,0)
        layout.oled.text("Hit",1,21)
        layout.oled.text("Stand",60,21)
        layout.oled.show()
        sleep(2)
        exec(open("Blackjack.py").read())
        show_menu(file_list)

    # This will allow for testing of all buttons and display
    if layout.button11.value() and layout.button22.value() and layout.button13.value():
        layout.oled.fill_rect(0,0,layout.width,layout.height,0)
        layout.oled.text("Test Device", 1, 10)
        layout.oled.show()
        sleep(1)
        exec(open("Test.py").read())
        show_menu(file_list)

    # This will launch the selected category
    if previous_value != layout.step_pin.value():
        if layout.step_pin.value() == False:

            # Turned Left
            if layout.direction_pin.value() == False:
                if highlight > 1:
                    highlight -= 1
                else:
                    if shift > 0:
                        shift -= 1

            # Turned Right
            else:
                if highlight < total_lines:
                    highlight += 1
                else:
                    if shift+total_lines < list_length:
                        shift += 1

            show_menu(file_list)
        previous_value = layout.step_pin.value()

    # Check for button pressed
    if layout.button_pin.value() == False and not button_down:
        button_down = True

        # Goes to function for running a category
        launch(file_list[(highlight-1) + shift])

    # Decbounce button
    if layout.button_pin.value() == True and button_down:
        button_down = False
