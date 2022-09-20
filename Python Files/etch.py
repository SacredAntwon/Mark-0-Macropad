from time import sleep
import layout

previous_value = True
direction_etch = True

invert = 0

etch_x = 0
etch_y = 0

drawList = []
elementList = []
button_bounce = True

layout.oled.fill_rect(0,0,layout.width,layout.height,0)
layout.oled.show()

while button_bounce:
    # Switch Directions
    if layout.button11.value():
        direction_etch = not direction_etch
        sleep(.25)
    
    # Invert Colors
    if layout.button21.value():
        invert = not invert
        layout.oled.invert(invert)
        sleep(.25)
    
    # Clear Screen
    if layout.button12.value():
        layout.oled.fill_rect(0,0,layout.width,layout.height,0)
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
        
    if previous_value != layout.step_pin.value():
        if layout.step_pin.value() == False:

            # Turned Left
            if layout.direction_pin.value() == False:
                if direction_etch: 
                    if etch_x > 0:
                        #print("L")
                        etch_x -= 1
                        elementList = [-5, 0]
                        drawList.append(elementList)
                else:
                    if etch_y < 31:
                        #print("D")
                        etch_y += 1
                        elementList = [0, 5]
                        drawList.append(elementList)
                
                
            # Turned Right
            else:
                if direction_etch:
                    
                    if etch_x < 127:
                        #print("R")
                        etch_x += 1
                        elementList = [5, 0]
                        drawList.append(elementList)
                else:
                    
                    if etch_y > 0:
                        #print("U")
                        etch_y -= 1
                        elementList = [0, -5]
                        drawList.append(elementList)
            
            layout.oled.pixel(etch_x, etch_y, 1)
            layout.oled.show()

        previous_value = layout.step_pin.value()
            
    if layout.button_pin.value() == False:
        layout.oled.fill_rect(0,0,layout.width,layout.height,0)
        layout.oled.invert(False)
        layout.oled.text("Going Back", 1, 10)
        layout.oled.text("To Menu", 1, 21)
        layout.oled.show()
        sleep(1)
        button_bounce = False
