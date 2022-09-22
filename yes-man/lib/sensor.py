import time
from lib.ringbuffer import RingBuffer
from machine import Pin, Timer
import micropython


class SyncingSensor():
    __syncFrequency = 5  # sensor pull frequency during sync
    __sensor = None  # sensor pin

    __syncCallbackRef = None  # method ref for ISR use
    __syncTimer = Timer()  # timer for sync pull
    __syncCount = 0  # number of HIGH-LOW patterns expected
    __synching = False  # state
    __syncBuffer = RingBuffer(500)  # buffer to pull sync data into from ISR
    __syncPattern = []  # list to hold number of consecutive same-value frames during sync

    __checkPatternRef = None  # method ref for ISR use

    __pulling = False  # state
    __pullTimer = Timer()  # timer used for actual data pull
    __pullCountPerDataFrame = const(1)  # amount of times the sensor is pulled per assumed data frame
    __pullLastValue = 0  # last value; used to detect EOT silence
    __pullNoChangeCount = 0  # length of current same-value stretch
    __maxNoChangeCount = const(10 * __pullCountPerDataFrame)  # max. length of same-value stretch until EOT is assumed

    __pullBuffer = RingBuffer(100)  # buffer for actual data (must be emptied from outside)

    def __init__(self, gpioPin, triggerOnFalling, syncCount=5, syncFrequency=100):
        print("SyncingSensor for PIN #" + str(gpioPin) + " Falling:" + str(triggerOnFalling) + " Count:" + str(syncCount) + ".")
        self.__sensor = Pin(gpioPin, Pin.IN, Pin.PULL_UP)
        # setup refs to methods, because creating them in ISRs is a no-no
        self.__syncCallbackRef = self.__isrPullSensorToSync
        self.__checkPatternRef = self.__checkPattern
        # set trigger as requested
        if triggerOnFalling:
            self.__sensor.irq(trigger=Pin.IRQ_FALLING, handler=self.__isrStartSyncingSensor)
        else:
            self.__sensor.irq(trigger=Pin.IRQ_RISING, handler=self.__isrStartSyncingSensor)
        # remember sync pattern count and frequency
        self.__syncCount = syncCount
        self.__syncFrequency = syncFrequency

    def __isrStartSyncingSensor(self, timer):
        # if already syncing or even pulling, abort
        if self.__synching or self.__pulling:
            return
        # track state
        self.__synching = True
        self.__pulling = False
        # capture sensor into buffer
        self.__syncBuffer.write(self.__sensor.value())
        # start (fast) timer for sync process
        self.__syncTimer.init(freq=self.__syncFrequency, mode=Timer.PERIODIC, callback=self.__syncCallbackRef)

    def __isrPullSensorToSync(self, timer):
        # if sync is over, kill timer
        if not self.__synching:
            self.__syncTimer.deinit()
            return
        # capture sensor into buffer
        self.__syncBuffer.write(self.__sensor.value())
        # delay data processing until after ISR
        micropython.schedule(self.__checkPatternRef, 0)

    def __checkPattern(self, args):
        # get all data from buffer
        while not self.__syncBuffer.isEmpty():
            self.__syncPattern.append(self.__syncBuffer.read())
        # figure out the amount of frames/pulls per value
        counts = self.__convertSyncPatternIntoCounts()
        # pattern complete and correct; switch to PULL mode
        if (self.__syncPatternHasEnoughIterations(counts) and self.__syncPatternCorrect(counts)):
            self.__synching = False
            self.__pulling = True
            self.__pullNoChangeCount = 0
            # calculate pull frequency and delay; wait for delay and start pulling
            pullFrequency = self.__syncFrequency / (sum(counts[:-1]) / (len(counts) - 1))
            time.sleep_ms(int(1000 / pullFrequency / self.__pullCountPerDataFrame / 2))
            self.__pullTimer.init(freq=int(pullFrequency * self.__pullCountPerDataFrame), mode=Timer.PERIODIC, callback=self.__isrPullSensorForData)
        # pattern at least one iteration long and already wrong; abort synching
        elif (len(counts) > 2) and not self.__syncPatternCorrect(counts[:-1]):
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
