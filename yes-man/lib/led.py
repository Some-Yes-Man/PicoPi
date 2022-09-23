from machine import Pin, Timer
import micropython


class Led:
    SPACE = const(" ")

    def __init__(self, gpioPin, freq=1, doneCallback=None):
        self.__led = Pin(gpioPin, Pin.OUT)
        self.__frequency = freq
        self.__blinking = False
        self.__timer = Timer()
        self.__sequence = []
        self.__index = 0
        self.__doneCallbackRef = doneCallback

    def blink(self, blinkString):
        self.__sequence.extend(list(blinkString))
        if (not self.__blinking):
            self.__blinking = True
            self.__timer.init(freq=self.__frequency, mode=Timer.PERIODIC, callback=self.__processSequence)

    def __processSequence(self, timer):
        if (self.__index == 0) and (len(self.__sequence) == 0):
            return
        if (self.__index < len(self.__sequence)):
            if (self.__sequence[self.__index] == Led.SPACE):
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
            if self.__doneCallbackRef is not None:
                micropython.schedule(self.__doneCallbackRef, 0)
