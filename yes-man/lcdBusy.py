import utime
import random
from machine import Pin, I2C
from pico_i2c_lcd import I2cLcd

running = True


def stopAll(irq):
    global running
    running = False


i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=10000)
lcd = I2cLcd(i2c, i2c.scan()[0], 2, 16)
lcd.clear()
lcd.backlight_on()

touchPin = Pin(16, Pin.IN, Pin.PULL_DOWN)
touchPin.irq(trigger=Pin.IRQ_RISING, handler=stopAll)


while running:
    lcd.putstr(str(random.randint(0, 9)))
    utime.sleep_ms(100)
