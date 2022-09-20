from time import sleep
import layout

page_one = ["A", "B", "C", "D", "E", "F"]
page_two = ["1", "2", "3", "4", "5", "6"]
all_pages = [page_one,page_two]

layout.oled.init_display()

def screen(page):
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

page = 0
total_page = 1

screen(0)

while button_bounce:
    if previous_value != layout.step_pin.value():
        if layout.step_pin.value() == False:

            # Turned Left
            if layout.direction_pin.value() == False:
                if page > 0:
                    page -= 1

            # Turned Right
            else:
                if page < total_page:
                    page += 1
            
            screen(page)
            sleep(.5)

        previous_value = layout.step_pin.value()
    
    layout.oled.fill_rect(0,0,layout.width,layout.height,0)
    layout.oled.show()
    
    while layout.button11.value():
        if page == 0:
            layout.k.press(0x04)
            layout.k.release(0x04)
        elif page == 1:
            layout.k.press(0x1e)
            layout.k.release(0x1e)
        layout.oled.text(all_pages[page][0],1,1)
        layout.oled.show()
        sleep(.1)
        
    while layout.button21.value():
        if page == 0:
            layout.k.press(0x05)
            layout.k.release(0x05)
        elif page == 1:
            layout.k.press(0x1f)
            layout.k.release(0x1f)
        layout.oled.text(all_pages[page][1],60,1)
        layout.oled.show()
        sleep(.1)
        
    while layout.button12.value():
        if page == 0:
            layout.k.press(0x06)
            layout.k.release(0x06)
        elif page == 1:
            layout.k.press(0x20)
            layout.k.release(0x20)
        layout.oled.text(all_pages[page][2],1,11)
        layout.oled.show()
        sleep(.1)
        
    while layout.button22.value():
        if page == 0:
            layout.k.press(0x07)
            layout.k.release(0x07)
        elif page == 1:
            layout.k.press(0x21)
            layout.k.release(0x21)
        layout.oled.text(all_pages[page][3],60,11)
        layout.oled.show()
        sleep(.1)
        
    while layout.button13.value():
        if page == 0:
            layout.k.press(0x08)
            layout.k.release(0x08)
        elif page == 1:
            layout.k.press(0x22)
            layout.k.release(0x22)
        layout.oled.text(all_pages[page][4],1,21)
        layout.oled.show()
        sleep(.1)
        
    while layout.button23.value():
        if page == 0:
            layout.k.press(0x09)
            layout.k.release(0x09)
        elif page == 1:
            layout.k.press(0x23)
            layout.k.release(0x23)
        layout.oled.text(all_pages[page][5],60,21)
        layout.oled.show()
        sleep(.1)
        
    if layout.button_pin.value() == False:
        layout.oled.fill_rect(0,0,layout.width,layout.height,0)
        layout.oled.text("Going Back", 1, 10)
        layout.oled.text("To Menu", 1, 21)
        layout.oled.show()
        sleep(1)
        button_bounce = False
