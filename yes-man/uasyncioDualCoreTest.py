import uasyncio
import _thread
import utime
from machine import Pin

running = True


async def secondCoreTask():
    while running:
        print("Task 2 re-scheduled to Core 1.")
        await uasyncio.sleep_ms(700)


def secondCoreInit():
    uasyncio.create_task(secondCoreTask())
    while running:
        print("Core 2 chilling.")
        utime.sleep_ms(500)


async def firstCoreTask():
    while running:
        print("Core 1 alive.")
        await uasyncio.sleep_ms(300)


def stop(irq):
    global running
    running = False


touchPin = Pin(16, Pin.IN, Pin.PULL_DOWN)
touchPin.irq(trigger=Pin.IRQ_RISING, handler=stop)

_thread.start_new_thread(secondCoreInit, ())

uasyncio.run(firstCoreTask())
