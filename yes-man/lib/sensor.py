from time import time
from machine import Pin, Timer
import micropython


def printFoo(args):
    print("foo")


class SyncingSensor():
    __syncFrequency = 200
    __sensor = None
    __pullTimer = Timer()
    __pulling = False
    __zeroPullCount = 0
    __syncTimer = Timer()
    __syncCount = 0
    __synching = False
    __syncPattern = []

    __printRef = None
    __theCounter = 0
    __theOtherCounter = 0
    __scheduled = False

    micropython.alloc_emergency_exception_buf(1000)

    def __init__(self, gpioPin, triggerOnFalling, syncCount=5):
        print("SyncingSensor for PIN #" + str(gpioPin) + " Falling: " + str(triggerOnFalling) + " Count: " + str(syncCount) + ".")
        self.__sensor = Pin(gpioPin, Pin.IN, Pin.PULL_UP)
        self.__printRef = printFoo
        print("foo: " + str(self.__synching) + " " + str(self.__pulling))
        if triggerOnFalling:
            self.__sensor.irq(trigger=Pin.IRQ_FALLING, handler=self.__startSyncingSensor)
        else:
            self.__sensor.irq(trigger=Pin.IRQ_RISING, handler=self.__startSyncingSensor)
        self.__syncCount = syncCount
        print("SyncingSensor done.")
        fooTimer = Timer()
        fooTimer.init(freq=0.2, mode=Timer.ONE_SHOT, callback=self.__foo)

    def __foo(self, timer):
        print("bar: " + str(self.__synching) + " " + str(self.__pulling) + " " + str(self.__theCounter) + " " + str(self.__scheduled) + " " + str(self.__theOtherCounter))

    def __printSyncStart(self, args):
        self.__scheduled = True
        # print("startSyncingSensor")

    def __startSyncingSensor(self, timer):
        self.__theCounter += 1
        if self.__synching or self.__pulling:
            return
        self.__theOtherCounter += 1
        micropython.schedule(self.__printRef, None)
        self.__synching = True
        self.__pulling = False
        #self.__syncPattern = [self.__sensor.value()]
        #self.__syncTimer.init(freq=self.__syncFrequency, mode=Timer.PERIODIC, callback=self.__pullSensorToSync)

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
        print("syncPull")
        if not self.__synching:
            self.__syncTimer.deinit()
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
            time.sleep_ms(1000 / pullFrequency / 2)
            self.__pullTimer.init(freq=pullFrequency, mode=Timer.PERIODIC, callback=self.__pullSensorForData)
        # pattern at least one iteration long and already wrong; abort synching
        elif (len(counts) > 2) and not self.__syncPatternCorrect(counts[:-1]):
            self.__synching = False
        # no conclusive result yet

    def __pullSensorForData(self, timer):
        print("dataPull")
        if not self.__pulling:
            self.__pullTimer.deinit()
            return
        value = self.__sensor.value()
        if (value == 1):
            self.__syncCount += 1
        else:
            self.__syncCount = 0
        if (self.__syncCount < 10):
            print(str(value))
        else:
            self.__pulling = False
