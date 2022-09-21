from machine import *
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from time import sleep_ms

i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
lcd = I2cLcd(i2c, 39, 2, 16)

def show(text):
    clear()
    lcd.putstr(text)

def show_in_loop(text):
    clear()
    if len(text) < 33:
        show(text)
        return
    current_first = 0
    for i in range(len(text)):
        end = min(len(text), current_first+32)
        text_to_show = text[current_first:end]
        if len(text_to_show) < 31:
            text_to_show += " -"
        if len(text_to_show) < 31:
            text_to_show += " " + text[:31-len(text_to_show)]
        show(text_to_show)
        current_first += 1
        sleep_ms(500)
    
def clear():
    lcd.clear()
    
def show_at(text, col, row):
    lcd.move_to(col, row)
    lcd.putstr(text)