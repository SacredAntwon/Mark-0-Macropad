# Author: Anthony Maida
# Purpose: Basic board information such as
# pins and screen size.

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from ws2812 import WS2812
import machine
import keyboard
import mouse
import consumer_control
import json

# Get save information
with open('JSONFiles/save.json', 'r') as f:
        saveJson = json.load(f)
        
# HID declarations
k = keyboard.Keyboard()
cc = consumer_control.Consumer_Control()
m = mouse.Mouse()

# LED pins
power = machine.Pin(11, machine.Pin.OUT)
power.value(1)
colorBrightness = float(saveJson['colorBrightness'])
led = WS2812(12, 1, colorBrightness)

# Screen setup and pins
screenBrightness = saveJson['screenBrightness']

width = 128
height = 32

id = 1
sda = Pin(6)
scl = Pin(7)

i2c = I2C(id=id, scl=scl, sda=sda)

oled = SSD1306_I2C(width=128, height=32, i2c=i2c)
oled.init_display()
oled.contrast(screenBrightness)

# Rotary encoder pins
buttonPin = Pin(27, Pin.IN, Pin.PULL_UP)
directionPin = Pin(26, Pin.IN, Pin.PULL_UP)
stepPin = Pin(28, Pin.IN, Pin.PULL_UP)

# Button pins
button11 = Pin(3, Pin.IN, Pin.PULL_DOWN)
button12 = Pin(4, Pin.IN, Pin.PULL_DOWN)
button13 = Pin(2, Pin.IN, Pin.PULL_DOWN)
button21 = Pin(29, Pin.IN, Pin.PULL_DOWN)
button22 = Pin(0, Pin.IN, Pin.PULL_DOWN)
button23 = Pin(1, Pin.IN, Pin.PULL_DOWN)
