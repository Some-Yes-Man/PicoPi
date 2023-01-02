import uasyncio
import _thread
import utime
from machine import Pin

running = True


async def secondTask():
    while running:
        print("Task 2.")
        await uasyncio.sleep_ms(700)


async def serviceTask():
    print("Service Task Start")
    while running:
        await uasyncio.sleep_ms(100)


def serviceCoreInit():
    print("Service Init")
    global serviceCoreTask
    serviceCoreTask = uasyncio.create_task(serviceTask())


async def mainTask():
    print("Main Task Start")
    while running:
        print("Main.")
        await uasyncio.sleep_ms(500)


def stop(irq):
    global running
    running = False


touchPin = Pin(16, Pin.IN, Pin.PULL_DOWN)
touchPin.irq(trigger=Pin.IRQ_RISING, handler=stop)

_thread.start_new_thread(serviceCoreInit, ())

someTask = uasyncio.create_task(secondTask())

uasyncio.run(mainTask())
