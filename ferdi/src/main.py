#from multiprocessing.queues import Queue

from machine import Pin, ADC
import time
from utime import sleep, sleep_ms
import _thread

import micropython

#from ferdi.src.event import event
from ferdi.src import EVENT_MAPPING
from ferdi.src.lightSensor import lightSensor
from ferdi.src.picoLedControl import picoLedControl
import uasyncio

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



#MainProcess()
#sthHappens()
#testInterrupt()


def testMultiSensor():
    #sender = picoLedControl(1, 'LED', Pin.OUT)
    #print("morse start")
    #_thread.start_new_thread(sender.morseSend,("Hello You", 200, Pin("LED", Pin.OUT)))
    #sender.morseSend ("Hello You ", 0.2)
    counter = 0
    #pin = Pin("LED", Pin.OUT)

    #_thread.start_new_thread(setValueTo1, ("LED", Pin.OUT))
    #setValueTo1(pin)

    while counter < 10:
        sleep(1)
        counter = counter + 1
        print("running")
    print("running is stopped")
    sleep(1)


#testMultiSensor()

mainOn = True
working = True

def theMainLoop():
    global mainOn
    pin = Pin("", 1)
    irq0 = pin.irq(trigger=pin.IRQ_RISING | pin.IRQ_FALLING,handler=setValueTo1("mainOn"))
    irq1 = pin.irq(trigger=pin.IRQ_RISING | pin.IRQ_FALLING,handler=setValueTo1("mainOn"))
    irq2 = pin.irq(trigger=pin.IRQ_RISING | pin.IRQ_FALLING,handler=setValueTo1("id1"))
    irq3 = pin.irq(trigger=pin.IRQ_RISING | pin.IRQ_FALLING,handler=setValueTo1("id2"))
    _thread.start_new_thread(hartAmWorken, ())

    while mainOn:
        sleep_ms(100)
        checkEventMappingsAndDoCb()



def checkEventMappingsAndDoCb():
    if EVENT_MAPPING.EVENT_MAPPING.values().__contains__(1):
        for key, value in EVENT_MAPPING.EVENT_MAPPING.items():
            if value == 1:
                uasyncio.create_task(EVENT_MAPPING.CB_MAPPING[key])



def setValueTo1(id):
    global mainOn, working
    if id == "mainOn":
        working = False
        mainOn = False
        return
    if id == "working":
        if working:
            working = False
            return
        else:
            working = True
            return
    else:
        if EVENT_MAPPING.EVENT_MAPPING[id] == 0:
            EVENT_MAPPING.EVENT_MAPPING[id] = 1
            return
        else:
            EVENT_MAPPING.EVENT_MAPPING[id] = 0
            return

    """
    /Me is worker and i do work!/
    """
def hartAmWorken():
    global working
    while working:
        await uasyncio.sleep_ms(200)
        print("still working...")
    print("no more working !")








