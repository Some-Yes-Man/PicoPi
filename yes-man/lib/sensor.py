from machine import Pin, Timer


class LightSensor:
    __baseFrequency = 100
    __sensor = None
    __timer = Timer()
    __count = 0
    __maxCount = 500

    def __init__(self, gpioPin):
        self.__sensor = Pin(gpioPin, Pin.IN, Pin.PULL_UP)
        self.__timer.init(
            freq=self.__baseFrequency, mode=Timer.PERIODIC, callback=self.__readSensor
        )

    def __readSensor(self, timer):
        self.__count += 1
        print(str(self.__count) + " : " + str(self.__sensor.value()))
        if (self.__count >= self.__maxCount):
            self.__timer.deinit()
