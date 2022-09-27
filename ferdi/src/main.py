#from multiprocessing.queues import Queue

from machine import Pin, ADC
import time
from utime import sleep
import _thread

import micropython

#from ferdi.src.event import event
from ferdi.src.lightSensor import lightSensor
from ferdi.src.picoLedControl import picoLedControl

micropython.alloc_emergency_exception_buf(100)

def MainProcess():

    #worker = _thread.start_new_thread(processEventOnQueue, events)
    while True:
        #Todo: sth happends -> event is created
        if sthHappens:
            pin = Pin(1, Pin.OUT)
            #e = event(pin)
            #events.put(e)
            counter = counter + 1
        if counter > 4:
            #worker.stopRunning()
            print("running is stopped")


def sthHappens():
    senderPin = Pin(1, Pin.OUT)
    dataPin = Pin(22, Pin.IN)
    sensor = lightSensor(dataPin)
    sender = picoLedControl(0, senderPin)
    receiver = picoLedControl(0, dataPin)
    worker = _thread.start_new_thread(sender.morseSend,("Hello You ", 0.2))
    #sender.morseSend("Hello You ", 0.5)
    print("morse send")
    #print("average is " + str(sensor.syncForMorse()))
    counter = 0
    result = []
    sensor.syncForMorse()
    while counter < 20:
        if not sensor.pollingState:

            result = receiver.morseReceive(sensor.duration, dataPin, 2)
            print(result)
            break
    print(receiver.morseToText(result))
    sensor.deInit()
    print("running is stopped")


def processEventOnQueue(events):
    curEvent = events.get(True, 100)
    curEvent.__call__()

def testInterrupt():
    pin = Pin(18, Pin.OUT)
    value = 0
    print(pin.value())
    pin.irq(trigger=pin.IRQ_RISING | pin.IRQ_FALLING,
                                 handler=lambda t:setValueTo1(value))
    counter = 0
    print('loop begins')
    while counter < 4:
        sleep(2)
        counter = counter +1
        print(value)
        if not value == 0:
            print(pin.value())
    pin.irq(trigger=pin.IRQ_RISING | pin.IRQ_FALLING,
                                 handler=None)
    print("running is stopped")

pin = Pin("LED", Pin.OUT)
def setValueTo1(pinName, state):
    #i = 0
    global pin
    # while i < 1:
    #     i += 1
    #     print("foo")
    #     time.sleep(1)
    # _thread.exit()
    # return
    #pin = Pin(pinName, state)
    time.sleep(1)
    #print("happend1")
    pin.value(0)
    #print("happend2")
    time.sleep(1)
    pin.value(1)
    time.sleep(1)
    pin.value(0)
    time.sleep(1)
    pin.value(1)
    #print("done")
    _thread.exit()
    return

#MainProcess()
#sthHappens()
#testInterrupt()
_thread.start_new_thread(setValueTo1, ("LED", Pin.OUT))

while True:
    time.sleep(1)
    print("running")
def testMultiSensor():
    #sender = picoLedControl(1, 'LED', Pin.OUT)
    #print("morse start")
    #_thread.start_new_thread(sender.morseSend,("Hello You", 200, Pin("LED", Pin.OUT)))
    #sender.morseSend ("Hello You ", 0.2)
    counter = 0
    #pin = Pin("LED", Pin.OUT)

    _thread.start_new_thread(setValueTo1, ("LED", Pin.OUT))
    #setValueTo1(pin)

    while counter < 10:
        sleep(1)
        counter = counter + 1
        print("running")
    print("running is stopped")
    sleep(1)


#testMultiSensor()






