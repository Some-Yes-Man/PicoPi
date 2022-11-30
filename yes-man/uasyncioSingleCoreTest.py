import uasyncio
import _thread
import utime
from machine import Pin

running = True


async def secondCoreTask():
    while running:
        print("Task re-scheduled to unused Core 2.")
        await uasyncio.sleep_ms(700)


async def firstCoreTask():
    while running:
        print("Core 1 alive.")
        utime.sleep_ms(300)


def stop(irq):
    global running
    running = False


touchPin = Pin(16, Pin.IN, Pin.PULL_DOWN)
touchPin.irq(trigger=Pin.IRQ_RISING, handler=stop)

# lands in scheduler first; so gets executed exactly once
task = uasyncio.create_task(secondCoreTask())

uasyncio.run(firstCoreTask())
