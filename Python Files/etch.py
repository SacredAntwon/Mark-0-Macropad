# Author: SacredAntwon
# Purpose: Drawing using the rotary encoder.

from time import sleep
import layout

# Initialize variables
previousValue = True
directionEtch = True

invert = 0

etchX = 0
etchY = 0

drawList = []
elementList = []
buttonBounce = True

# Clear screen
layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
layout.oled.show()

while buttonBounce:
    # Switch Directions
    if layout.button11.value():
        directionEtch = not directionEtch
        sleep(.25)

    # Invert Colors
    if layout.button21.value():
        invert = not invert
        layout.oled.invert(invert)
        sleep(.25)

    # Clear Screen
    if layout.button12.value():
        layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
        layout.oled.show()
        drawList = []
        sleep(.25)

    # Draw on PC
    if layout.button22.value():
        layout.m.press(layout.m.BUTTON_LEFT)
        for position in drawList:
            layout.m.move(position[0], position[1])
        layout.m.release(layout.m.BUTTON_LEFT)
        sleep(.25)

    if previousValue != layout.stepPin.value():
        if layout.stepPin.value() == False:

            # Turned rotary encoder left
            if layout.directionPin.value() == False:
                if directionEtch:
                    # Draw left
                    if etchX > 0:
                        etchX -= 1
                        elementList = [-5, 0]
                        drawList.append(elementList)
                else:
                    # Draw down
                    if etchY < 31:
                        etchY += 1
                        elementList = [0, 5]
                        drawList.append(elementList)

            # Turned rotary encoder right
            else:
                if directionEtch:
                    # Draw right
                    if etchX < 127:
                        etchX += 1
                        elementList = [5, 0]
                        drawList.append(elementList)
                else:
                    # Draw up
                    if etchY > 0:
                        etchY -= 1
                        elementList = [0, -5]
                        drawList.append(elementList)

            # Display the pixel
            layout.oled.pixel(etchX, etchY, 1)
            layout.oled.show()

        previousValue = layout.stepPin.value()

    # Back to menu
    if layout.buttonPin.value() == False:
        layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
        layout.oled.invert(False)
        layout.oled.text("Going Back", 1, 10)
        layout.oled.text("To Menu", 1, 21)
        layout.oled.show()
        sleep(1)
        buttonBounce = False
