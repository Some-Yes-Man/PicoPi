

from machine import Timer
import utime
class lightSensor:

    def __init__(self, pin):
        self.pin = pin
        self.pollingState = True
        self.received = []
        self.times = []
        self.interrupt = pin.irq(trigger=pin.IRQ_RISING | pin.IRQ_FALLING,
                                 handler=lambda t: self.syncForMorse() if self.pollingState else None)
        self.lastTime = utime.ticks_ms()
        self.prevValue = 0
        self.duration = 0


    def syncForMorse(self):
        cur = self.pin.value()
        #print("interrupted")
        if cur == self.prevValue:
            #print('ignored')
            return
        newTime = utime.ticks_ms()
        timeDiff = newTime - self.lastTime
        if timeDiff > 50000000:
            print('took too long: '+ str(newTime)+", "+str(self.lastTime))
            return
        self.lastTime = newTime
        if len(self.received) > 6:
            if self.isCorrectStart():
                print('average is :' + str(self.averageTimes()))
                self.pollingState = False
                return self.averageTimes()
        else:
            self.received.append(cur)
            self.times.append(timeDiff)
            self.prevValue = cur
            return

    def isCorrectStart(self):
        if self.received == [1,0,1,0,1,0,1] or self.received == [0,1,0,1,0,1,0]:
            return True
        return False

    def averageTimes(self):
        print(self.times)
        size = len(self.times)
        self.duration = sum(self.times)/size
        return self.duration

    def deInit(self):
        self.interrupt = self.pin.irq(trigger=self.pin.IRQ_RISING | self.pin.IRQ_FALLING,
                                 handler=None)
        self.received = []
        self.times = []
        print('de_init happend')

