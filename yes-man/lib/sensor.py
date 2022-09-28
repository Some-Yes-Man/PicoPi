from lib.ringbuffer import RingBuffer
from machine import Pin, Timer
import micropython


class SyncingSensor():
    pullCountPerDataFrame = const(4)  # amount of times the sensor is pulled per assumed data frame
    maxNoChangeCount = const(10)  # max. length of same-value stretch until EOT is assumed

    def __init__(self, gpioPin, triggerOnFalling, syncCount=5, syncFrequency=100, invertSignal=False):
        print("SyncingSensor for PIN #" + str(gpioPin) + " Falling:" + str(triggerOnFalling) + " Count:" + str(syncCount) + ".")
        self.__sensor = Pin(gpioPin, Pin.IN, Pin.PULL_UP)  # sensor pin
        # setup refs to methods, because creating them in ISRs is a no-no
        self.__syncCallbackRef = self.__isrPullSensorToSync  # method ref for ISR use
        self.__checkPatternRef = self.__checkPattern  # method ref for ISR use
        # set trigger as requested
        if triggerOnFalling:
            self.__sensor.irq(trigger=Pin.IRQ_FALLING, handler=self.__isrStartSyncingSensor)
        else:
            self.__sensor.irq(trigger=Pin.IRQ_RISING, handler=self.__isrStartSyncingSensor)

        self.__syncCount = syncCount  # number of HIGH-LOW patterns expected
        self.__syncFrequency = syncFrequency  # sensor pull frequency during sync
        self.__syncTimer = Timer()  # timer for sync pull
        self.__synching = False  # state
        self.__syncBuffer = RingBuffer(500)  # buffer to pull sync data into from ISR
        self.__syncPattern = []  # list to hold number of consecutive same-value frames during sync
        self.__pulling = False  # state
        self.__pullTimer = Timer()  # timer used for actual data pull
        self.__pullLastValue = 0  # last value; used to detect EOT silence
        self.__pullNoChangeCount = 0  # length of current same-value stretch
        self.__pullFrameDiff = 0  # size diff of current pull frame (+/- 1)
        self.__pullFrameIndex = 0  # filled slots in current pull frame
        self.__pullFrameBuffer = bytearray(SyncingSensor.pullCountPerDataFrame + 1)  # current pull frame
        self.__pullBuffer = RingBuffer(100)  # buffer for actual data (must be emptied from outside)
        self.__invertSignal = invertSignal

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
            self.__pullTimer.init(freq=int(pullFrequency * SyncingSensor.pullCountPerDataFrame), mode=Timer.PERIODIC, callback=self.__isrPullSensorForData)
        # pattern at least one iteration long and already wrong; abort synching
        elif (len(counts) > 3) and not self.__syncPatternCorrect(counts[:-1]):
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
        return (max(pattern) - min(pattern) <= 2) and (pattern[len(pattern) - 1] >= min(pattern[:-1]))

    def __isrPullSensorForData(self, timer):
        if not self.__pulling:
            self.__pullTimer.deinit()
            return
        # go through pull frame first
        self.__pullFrameBuffer[self.__pullFrameIndex] = self.__sensor.value()
        self.__pullFrameIndex += 1
        # check whether frame is complete
        if (self.__pullFrameIndex >= (SyncingSensor.pullCountPerDataFrame + self.__pullFrameDiff)):
            # print("FULL " + str(self.__pullFrameBuffer)+" i:" + str(self.__pullFrameIndex) + " d:" + str(self.__pullFrameDiff))
            # check for 'one'
            if (sum(self.__pullFrameBuffer) >= (SyncingSensor.pullCountPerDataFrame + self.__pullFrameDiff - 1)):
                value = 1
            # zero
            else:
                value = 0
            # only for 'normal' frames check start+end
            if (self.__pullFrameIndex == SyncingSensor.pullCountPerDataFrame):
                if (self.__pullFrameBuffer[0] != value):
                    # print("+1")
                    self.__pullFrameDiff = 1
                if (self.__pullFrameBuffer[SyncingSensor.pullCountPerDataFrame - 1] != value):
                    # print("-1")
                    self.__pullFrameDiff = -1
            else:
                # print("=0")
                self.__pullFrameDiff = 0
            # zero-out frame; reset
            for i in range(SyncingSensor.pullCountPerDataFrame):
                self.__pullFrameBuffer[i] = 0
            self.__pullFrameIndex = 0
            # check for signal changes to determine EOT
            if (value == self.__pullLastValue):
                self.__pullNoChangeCount += 1
            else:
                self.__pullNoChangeCount = 0
                self.__pullLastValue = value
            if (self.__pullNoChangeCount < SyncingSensor.maxNoChangeCount):
                if self.__invertSignal:
                    self.__pullBuffer.write(1 - value)
                else:
                    self.__pullBuffer.write(value)
            else:
                self.__pulling = False

    def readBuffer(self):
        return self.__pullBuffer.read()

    def isBufferEmpty(self):
        return self.__pullBuffer.isEmpty()

    def shutdown(self):
        self.__sensor.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=None)
        self.__pulling = False
        self.__synching = False
