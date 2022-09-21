from machine import Pin, Timer
import micropython


class Led:
    SPACE = const(" ")
    __frequency = 1
    __blinking = False
    __timer = Timer()
    __led = None
    __sequence = []
    __index = 0

    def __init__(self, gpioPin, freq=None):
        if (freq is not None):
            self.__frequency = freq
        self.__led = Pin(gpioPin, Pin.OUT)

    def blink(self, blinkString):
        self.__sequence.extend(list(blinkString))
        if (not self.__blinking):
            self.__blinking = True
            self.__timer.init(freq=self.__frequency, mode=Timer.PERIODIC, callback=self.__processSequence)

    def __processSequence(self, timer):
        if (self.__index == 0) and (len(self.__sequence) == 0):
            return
        if (self.__index < len(self.__sequence)):
            if (self.__sequence[self.__index] == self.SPACE):
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
