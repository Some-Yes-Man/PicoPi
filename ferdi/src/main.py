from queue import Queue

from machine import Pin
from utime import sleep
import _thread

from event import event
from picoLedControl import picoLedControl



def MainProcess():
    counter = 0
    events = Queue()
    worker = _thread.start_new_thread(processEventOnQueue, events)
    while True:
        #Todo: sth happends -> event is created
        if sthHappens:
            pin = Pin(1, Pin.OUT)
            e = event(pin)
            events.put(e)
            counter = counter +1
        if counter > 4:
            worker.stopRunning()
            print("running is stopped")


def sthHappens():
    return True

def processEventOnQueue(events):
    curEvent = events.get(True, 100)
    curEvent.__call__()


MainProcess()





