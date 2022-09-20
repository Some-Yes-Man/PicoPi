import time
from lib.led import Led
from lib.morse import Morse
from lib.sensor import SyncingSensor

m = Morse()
l = Led(gpioPin=0, freq=20)
s = SyncingSensor(gpioPin=28, triggerOnFalling=True)

blinkCode = m.toBlink("^my display is broken -.-")
print(blinkCode)
l.blink(blinkCode)

while True:
    time.sleep(1)
    print("tick")
