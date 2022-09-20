from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from time import sleep
import machine
import keyboard
import mouse
import consumer_control

# HID declarations
k = keyboard.Keyboard()
cc = consumer_control.Consumer_Control()
m = mouse.Mouse()

# Screen setup and pins
width = 128
height = 32

id = 1
sda = Pin(6)
scl = Pin(7)

i2c = I2C(id=id, scl=scl, sda=sda)

oled = SSD1306_I2C(width=128, height=32, i2c=i2c)

# Rotary encoder pins
button_pin = Pin(27, Pin.IN, Pin.PULL_UP)
direction_pin = Pin(26, Pin.IN, Pin.PULL_UP)
step_pin  = Pin(28, Pin.IN, Pin.PULL_UP)

# Button pins
button11 = Pin(3, Pin.IN, Pin.PULL_DOWN)
button12 = Pin(4, Pin.IN, Pin.PULL_DOWN)
button13 = Pin(2, Pin.IN, Pin.PULL_DOWN)
button21 = Pin(29, Pin.IN, Pin.PULL_DOWN)
button22 = Pin(0, Pin.IN, Pin.PULL_DOWN)
button23 = Pin(1, Pin.IN, Pin.PULL_DOWN)
