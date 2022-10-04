#from multiprocessing.queues import Queue

from machine import Pin
from utime import sleep, sleep_ms
import _thread

import micropython

from ferdi.src.EVENT_MAPPING import THE_EVENT_MAPPING
from ferdi.src.lightSensor import lightSensor
from ferdi.src.picoLedControl import picoLedControl
import uasyncio

from ferdi.src.callBacks import CB_MAPPING

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
    #worker = _thread.start_new_thread(sender.morseSend,("Hello You ", 0.2))
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
    pin = Pin(18, Pin.IN)
    print("value: " + str(pin.value()))
    #pin.irq(trigger=pin.IRQ_RISING | pin.IRQ_FALLING,
                                 #handler=lambda t:setValueTo1(value))
    counter = 0
    print('loop begins')
    while counter < 10:
        sleep(1)
        counter = counter +1
        print("value: " + str(pin.value()))
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
    global mainOn, working, THE_EVENT_MAPPING
    pin = Pin("LED", Pin.OUT)
    pin_ = Pin(18, Pin.IN)
    #pin.irq(trigger=pin.IRQ_RISING | pin.IRQ_FALLING,handler=setValueTo1("mainOn"))
    #pin.irq(trigger=pin.IRQ_RISING | pin.IRQ_FALLING,handler=setValueTo1("working"))
    pin_.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=setValueTo1)
    #pin_.irq(trigger=pin_.IRQ_RISING,handler=setValueTo1("id2"))
    #_thread.start_new_thread(initSecondCore, ())
    counter = 0
    while mainOn:
        sleep_ms(100)
        checkEventMappingsAndDoCallbacks()
        counter = counter + 1
        #print("main is running")
        if counter == 200:
            setValueTo1("working")
            sleep_ms(1000)
            setValueTo1("mainOn")
    print("We are completely done !")


def checkEventMappingsAndDoCallbacks():
    if 1 in THE_EVENT_MAPPING.values():
        for key, value in THE_EVENT_MAPPING.items():
            if value == 1:
                print(callable(CB_MAPPING[key]))
                uasyncio.create_task(CB_MAPPING[key]())


def setValueTo1(irq):
    global mainOn, working, THE_EVENT_MAPPING
    irqId = "id1"
    if irqId == 1:
        working = False
        mainOn = False
        return
    else:
        if irqId == 2:
            if working:
                working = False
                return
            else:
                working = True
                return
        else:
            if THE_EVENT_MAPPING[irqId] == 0:
                THE_EVENT_MAPPING[irqId] = 1
                #print("set 1")
                return
            else:
                THE_EVENT_MAPPING[irqId] = 0
                #print("set 0")
                return


"""
    /Me is worker and i do my work!/
"""
async def hartAmWorken():
    global working
    while working:
        await uasyncio.sleep_ms(500)
        print("still working...")
    print("no more working !")


def initSecondCore():
    global working
    uasyncio.run(hartAmWorken())

theMainLoop()
