# Author: Anthony Maida
# Purpose: Display logo.

import framebuf
import layout
from time import sleep

# Get LED
led = layout.led

# Add all images to the buffer and store in list
images = []
for n in range(1, 28):
    with open('/LogoAnimation/image%s.pbm' % n, 'rb') as f:  #open folder and image
        f.readline() # Magic number
        f.readline() # Creator comment
        f.readline() # Dimensions
        data = bytearray(f.read())
    
    fbuf = framebuf.FrameBuffer(data, 128, 32, framebuf.MONO_HLSB) #adjust accordingly the width and height
    images.append(fbuf)

# Display logo and colors
colorNum = 1
for i in images[1::]:
    layout.oled.blit(i, 0, 0)
    layout.oled.show()
    led.pixels_set(0, led.wheel(colorNum & 255))
    led.pixels_show()
    colorNum += 7
    sleep(0.10)

