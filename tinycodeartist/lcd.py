from machine import *
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
lcd = I2cLcd(i2c, 39, 2, 16)

def show(text):
    clear()
    lcd.putstr(text)
    
def clear():
    lcd.clear()
    
def show_at(text, col, row):
    lcd.move_to(col, row)
    lcd.putstr(text)