
from machine import Pin, ADC
from utime import sleep
import _thread

#from ferdi.src.event import event
from ferdi.src.lightSensor import lightSensor
from ferdi.src.picoLedControl import picoLedControl


# def MainProcess():
#     counter = 0
#     events = Queue()
#     worker = _thread.start_new_thread(processEventOnQueue, events)
#     while True:
#         #Todo: sth happends -> event is created
#         if sthHappens:
#             pin = Pin(1, Pin.OUT)
#             e = event(pin)
#             events.put(e)
#             counter = counter +1
#         if counter > 4:
#             worker.stopRunning()
#             print("running is stopped")


def sthHappens():
    dataPin = Pin(22, Pin.IN)
    print(dataPin.value())
    sensor = lightSensor(dataPin)
    ledReader = picoLedControl(0, dataPin)
    #print("average is " + str(sensor.syncForMorse()))
    counter = 0
    result = []
    while counter < 4:
        sleep(2)
        counter = counter +1
        if not sensor.pollingState:
            result = ledReader.morseReceive(sensor.duration, dataPin, 2)
            print(result)
            break
    print(ledReader.morseToText(result))
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


def setValueTo1(value):
   value = 1

#MainProcess()
sthHappens()
#testInterrupt()





