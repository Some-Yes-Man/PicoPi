from machine import Pin, I2C
from pico_i2c_lcd import I2cLcd


def printDisplay(pin):
    global row
    global line
    # lcd.show_cursor()
    # lcd.blink_cursor_on()
    # lcd.backlight_off()
    # lcd.display_off()
    lcd.move_to(0, row)
    lcd.putstr("                ")
    lcd.move_to(0, row)
    lcd.putstr(lines[line])
    row = (row + 1) % 2
    line = (line + 1) % len(lines)


heart = (0x00, 0x00, 0x1B, 0x1F, 0x0E, 0x04, 0x00, 0x00)
smiley = (0x00, 0x0A, 0x00, 0x04, 0x04, 0x11, 0x0E, 0x00)
space1 = (0x00, 0x02, 0x07, 0x0D, 0x1F, 0x17, 0x14, 0x02)
space2 = (0x00, 0x08, 0x1C, 0x16, 0x1F, 0x1D, 0x05, 0x08)
symbols = (heart, smiley, space1, space2)
line_lisa = "PAPA " + chr(0) + " LISA"
line_maggie = "PAPA " + chr(0) + " MAGGIE"
line_mama = "PAPA " + chr(0) + " MAMA"
lines = (line_lisa, line_maggie, line_mama)
row = 0
line = 0


i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
lcd = I2cLcd(i2c, i2c.scan()[0], 2, 16)
lcd.clear()
lcd.backlight_on()
for symIndex in range(len(symbols)):
    lcd.custom_char(symIndex, symbols[symIndex])

touchPin = Pin(16, Pin.IN, Pin.PULL_DOWN)
touchPin.irq(trigger=Pin.IRQ_RISING, handler=printDisplay)
