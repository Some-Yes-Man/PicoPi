import time
from lib.ringbuffer import RingBuffer
from machine import Pin, Timer
import micropython


class SyncingSensor():
    __syncFrequency = 5
    __sensor = None

    __syncCallbackRef = None
    __syncTimer = Timer()
    __syncCount = 0
    __synching = False
    __syncBuffer = RingBuffer(500)
    __syncPattern = []

    __checkPatternRef = None

    __pulling = False
    __pullTimer = Timer()
    __pullLastValue = 0
    __pullNoChangeCount = 0
    __maxNoChangeCount = 10

    __pullBuffer = RingBuffer(100)

    def __init__(self, gpioPin, triggerOnFalling, syncCount=5, syncFrequency=100):
        print("SyncingSensor for PIN #" + str(gpioPin) + " Falling:" + str(triggerOnFalling) + " Count:" + str(syncCount) + ".")
        self.__sensor = Pin(gpioPin, Pin.IN, Pin.PULL_UP)
        self.__syncCallbackRef = self.__isrPullSensorToSync
        self.__checkPatternRef = self.__checkPattern
        if triggerOnFalling:
            self.__sensor.irq(trigger=Pin.IRQ_FALLING, handler=self.__isrStartSyncingSensor)
        else:
            self.__sensor.irq(trigger=Pin.IRQ_RISING, handler=self.__isrStartSyncingSensor)
        self.__syncCount = syncCount
        self.__syncFrequency = syncFrequency

    def __isrStartSyncingSensor(self, timer):
        if self.__synching or self.__pulling:
            return
        self.__synching = True
        self.__pulling = False
        self.__syncBuffer.write(self.__sensor.value())
        self.__syncTimer.init(freq=self.__syncFrequency, mode=Timer.PERIODIC, callback=self.__syncCallbackRef)

    def __isrPullSensorToSync(self, timer):
        if not self.__synching:
            self.__syncTimer.deinit()
            return
        self.__syncBuffer.write(self.__sensor.value())
        micropython.schedule(self.__checkPatternRef, 0)

    def __checkPattern(self, args):
        while not self.__syncBuffer.isEmpty():
            self.__syncPattern.append(self.__syncBuffer.read())
        counts = self.__convertSyncPatternIntoCounts()
        # pattern complete and correct; switch to PULL mode
        if (self.__syncPatternHasEnoughIterations(counts) and self.__syncPatternCorrect(counts)):
            print("switch")
            self.__synching = False
            self.__pulling = True
            # calculate pull frequency and delay; wait for delay and start pulling
            pullFrequency = self.__syncFrequency / (sum(counts[:-1]) / (len(counts) - 1))
            time.sleep_ms(int(1000 / pullFrequency / 2))
            print("freq: " + str(pullFrequency))
            print("offs: " + str(int(1000 / pullFrequency / 2)))
            self.__pullNoChangeCount = 0
            self.__pullTimer.init(freq=pullFrequency, mode=Timer.PERIODIC, callback=self.__isrPullSensorForData)
        # pattern at least one iteration long and already wrong; abort synching
        elif (len(counts) > 2) and not self.__syncPatternCorrect(counts[:-1]):
            print("abort")
            self.__synching = False
            self.__syncPattern.clear()
        # no conclusive result yet

    def __convertSyncPatternIntoCounts(self):
        iterationIndex = -1
        symbolIndex = -1
        lastSymbol = None
        symbolCounts = []
        # check whole pattern
        for symbol in self.__syncPattern:
            # every time the current state changes
            if (symbol != lastSymbol):
                symbolIndex = (symbolIndex + 1) % 2
                symbolCounts.append(1)
                # every other state change
                if (symbolIndex == 0):
                    iterationIndex += 1
                lastSymbol = symbol
            else:
                symbolCounts[iterationIndex * 2 + symbolIndex] += 1
        print(symbolCounts)
        return symbolCounts

    def __syncPatternHasEnoughIterations(self, pattern):
        return len(pattern) == 2 * self.__syncCount

    def __syncPatternCorrect(self, pattern):
        return max(pattern) - min(pattern) <= 2

    def __isrPullSensorForData(self, timer):
        if not self.__pulling:
            self.__pullTimer.deinit()
            return
        value = self.__sensor.value()
        if (value == self.__pullLastValue):
            self.__pullNoChangeCount += 1
        else:
            self.__pullNoChangeCount = 0
            self.__pullLastValue = value
        if (self.__pullNoChangeCount < self.__maxNoChangeCount):
            self.__pullBuffer.write(value)
        else:
            self.__pulling = False

    def readBuffer(self):
        return self.__pullBuffer.read()

    def isBufferEmpty(self):
        return self.__pullBuffer.isEmpty()
