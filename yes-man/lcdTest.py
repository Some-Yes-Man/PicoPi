from machine import Pin, I2C
from pico_i2c_lcd import I2cLcd
from time import sleep_ms


def printDisplay(pin):
    lcd.clear()
    lcd.show_cursor()
    lcd.blink_cursor_on()
    lcd.custom_char(0, space1)
    lcd.custom_char(1, space2)
    lcd.putstr("Invader")
    lcd.move_to(7, 1)
    lcd.putstr(chr(0) + chr(1))


i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
lcd = I2cLcd(i2c, i2c.scan()[0], 2, 16)
lcd.clear()
heart = (0x00, 0x00, 0x1B, 0x1F, 0x0E, 0x04, 0x00, 0x00)
smiley = (0x00, 0x0A, 0x00, 0x04, 0x04, 0x11, 0x0E, 0x00)
space1 = (0x00, 0x02, 0x07, 0x0D, 0x1F, 0x17, 0x14, 0x02)
space2 = (0x00, 0x08, 0x1C, 0x16, 0x1F, 0x1D, 0x05, 0x08)

touchPin = Pin(16, Pin.IN, Pin.PULL_DOWN)
touchPin.irq(trigger=Pin.IRQ_RISING, handler=printDisplay)
