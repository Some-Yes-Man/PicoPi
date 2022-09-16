from machine import Pin, Timer


class LightSensor:
    __pullFrequency = 200
    __sensor = None
    __timer = Timer()
    __pulling = False
    __synching = False
    __syncPattern = []

    __count = 0
    __maxCount = 500

    def __init__(self, gpioPin):
        self.__sensor = Pin(gpioPin, Pin.IN, Pin.PULL_UP)
        self.__sensor.irq(Pin.IRQ_FALLING, self.__syncSensor)
        self.__timer.init(freq=self.__pullFrequency, mode=Timer.PERIODIC, callback=self.__readSensor)

    def __syncSensor(self, timer):
        self.__synching = True
        self.__pulling = False
        self.__syncPattern = []

    def __readSensor(self, timer):
        if self.__synching:
            self.__syncPattern + self.__sensor.value()
            return
        if not self.__pulling:
            return
        self.__count += 1
        print(str(self.__count) + " : " + str(self.__sensor.value()))
        if (self.__count >= self.__maxCount):
            self.__timer.deinit()
