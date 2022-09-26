import time
import _thread
import random
from machine import Pin, I2C
from pico_i2c_lcd import I2cLcd
from lib.led import Led
from lib.morse import Morse
from lib.sensor import SyncingSensor

runningOne = True
runningTwo = True


def sndCoreTask():
    global runningOne

    i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=10000)
    lcd = I2cLcd(i2c, i2c.scan()[0], 2, 16)
    lcd.clear()
    lcd.backlight_on()
    lcd.putstr(str(random.randint(100, 999)) + " ")

    sensor = SyncingSensor(gpioPin=28, triggerOnFalling=True, syncCount=5, syncFrequency=200, invertSignal=True)
    currentRead = []

    while runningTwo:
        while not sensor.isBufferEmpty():
            print("#")
            # print(s.readBuffer())
            signal = sensor.readBuffer()
            # don't read ZEROs at start of sequence
            if ((len(currentRead) > 0) or (signal != 0)):
                currentRead.append(signal)
            # look for end of word
            if ((len(currentRead[-7:]) == 7) and (sum(currentRead[-7:]) == 0)):
                lcd.putstr(" ")
                currentRead.clear()
            # look for end of letter
            elif ((len(currentRead[-3:]) == 3) and (sum(currentRead[-3:]) == 0)):
                blink = ""
                for bit in currentRead[:-3]:
                    if (bit == 0):
                        blink += " "
                    else:
                        blink += "#"
                lcd.putstr(Morse.toLetterFromBlink(blink))
                currentRead.clear()
        time.sleep_ms(100)
    # set flag to shut down core #0
    runningOne = False
    _thread.exit()


def stopCores(timer):
    global runningTwo
    runningTwo = False


led = Led(gpioPin=0, freq=30)
blinkCode = Morse.toBlink("^what hath god wrought!")
print(blinkCode)
led.blink(blinkCode)

touchPin = Pin(16, Pin.IN, Pin.PULL_DOWN)
touchPin.irq(trigger=Pin.IRQ_RISING, handler=stopCores)

_thread.start_new_thread(sndCoreTask, ())

while runningOne:
    print("Running...")
    time.sleep_ms(1000)

print("Done.")
