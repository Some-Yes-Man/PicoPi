import time
from lib.led import Led
from lib.morse import Morse
from lib.sensor import SyncingSensor

m = Morse()
l = Led(gpioPin=0, freq=17)
s = SyncingSensor(gpioPin=28, triggerOnFalling=True, syncCount=5, syncFrequency=100)

blinkCode1 = m.toBlink("^display ")
blinkCode2 = m.toBlink("broke -.-")
print(blinkCode1)
print(blinkCode2)
l.blink(blinkCode1)
l.blink(blinkCode2)

while True:
    while not s.isBufferEmpty():
        print(s.readBuffer())
    time.sleep_ms(500)
