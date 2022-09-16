from time import time
from machine import Pin, Timer


class Sensor():
    __syncFrequency = 200
    __sensor = None
    __pullTimer = Timer()
    __pulling = False
    __syncTimer = Timer()
    __syncCount = 0
    __synching = False
    __syncPattern = []

    def __init__(self, gpioPin, triggerOnFalling, syncCount=5):
        self.__sensor = Pin(gpioPin, Pin.IN)  # Pin.PULL_UP
        if triggerOnFalling:
            self.__sensor.irq(Pin.IRQ_FALLING, self.__startSyncingSensor)
        else:
            self.__sensor.irq(Pin.IRQ_RISING, self.__startSyncingSensor)
        self.__syncCount = syncCount

    def __startSyncingSensor(self, timer):
        if self.__synching or self.__pulling:
            return
        self.__synching = True
        self.__pulling = False
        self.__syncPattern = [self.__sensor.value()]
        self.__syncTimer.init(freq=self.__syncFrequency, mode=Timer.PERIODIC, callback=self.__pullSensorToSync)

    def __convertSyncPatternIntoCounts(self):
        iterationIndex = -1
        symbolIndex = -1
        symbol = None
        symbolCounts = []
        # check whole pattern
        for patternIndex in range(len(self.__syncPattern)):
            # every time the current state changes
            if (self.__syncPattern[patternIndex] != symbol):
                symbolIndex = (symbolIndex + 1) % 2
                symbolCounts.append(1)
                # every other state change
                if (symbolIndex == 0):
                    iterationIndex += 1
                symbol = self.__syncPattern[patternIndex]
            else:
                symbolCounts[iterationIndex * 2 + symbolIndex] += 1
        return symbolCounts

    def __syncPatternHasEnoughIterations(self, pattern):
        return len(pattern) == 2 * self.__syncCount

    def __syncPatternCorrect(self, pattern):
        return max(pattern) - min(pattern) <= 1

    def __pullSensorToSync(self, timer):
        if not self.__synching:
            return
        # pull sensor values and create pattern
        self.__syncPattern.append(self.__sensor.value())
        counts = self.__convertSyncPatternIntoCounts()
        # pattern complete and correct; switch to PULL mode
        if (self.__syncPatternHasEnoughIterations(counts) and self.__syncPatternCorrect(counts)):
            self.__synching = False
            self.__pulling = True
            # calculate pull frequency and delay; wait for delay and start pulling
            pullFrequency = self.__syncFrequency / (sum(counts) / len(counts))
            time.sleep_ms(1 / pullFrequency / 2)
            self.__pullTimer.init(freq=pullFrequency, mode=Timer.PERIODIC, callback=self.__pullSensorForData)
        # pattern at least one iteration long and already wrong; abort synching
        elif (len(counts) > 2) and not self.__syncPatternCorrect(counts[:-1]):
            self.__synching = False
        # no conclusive result yet

    def __pullSensorForData(self, timer):
        return
