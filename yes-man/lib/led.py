from machine import Pin, Timer
import micropython


class Led:
    __frequency = 1
    __blinking = False
    __timer = Timer()
    __led = None
    __sequence = []
    __index = 0

    micropython.alloc_emergency_exception_buf(100)

    def __init__(self, gpioPin, freq=None):
        if (freq != None):
            self.__frequency = freq
        self.__led = Pin(gpioPin, Pin.OUT)

    def blink(self, blinkString):
        if (not self.__blinking):
            self.__blinking = True
            self.__timer.init(freq=self.__frequency, mode=Timer.PERIODIC, callback=self.__processSequence,)
        self.__sequence.extend(list(blinkString))

    def __processSequence(self, timer):
        if (self.__index == 0) and (len(self.__sequence) == 0):
            return
        if (self.__index < len(self.__sequence)):
            if (self.__sequence[self.__index] == " "):
                self.__led.off()
            else:
                self.__led.on()
            self.__index += 1
        else:
            self.__sequence.clear()
            self.__index = 0
            self.__blinking = False
            self.__timer.deinit()
            self.__led.off()
