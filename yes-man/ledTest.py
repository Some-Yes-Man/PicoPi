import time
from lib.led import Led
from lib.morse import Morse
from lib.sensor import SyncingSensor

m = Morse()
led1 = Led(gpioPin=0, freq=3, doneCallback=lambda x: led2.blink(blinkCode2))
led2 = Led(gpioPin=0, freq=2.9, doneCallback=lambda x: led3.blink(blinkCode3))
led3 = Led(gpioPin=0, freq=3.1)
s = SyncingSensor(gpioPin=28, triggerOnFalling=True, syncCount=5, syncFrequency=10, invertSignal=True)

blinkCode1 = m.toBlink("^")
blinkCode2 = m.toBlink("sos")
blinkCode3 = m.toBlink(" sos")
print(blinkCode1)
print(blinkCode2)
print(blinkCode3)
led1.blink(blinkCode1)

while True:
    while not s.isBufferEmpty():
        print(">>>>> " + str(s.readBuffer()))
    time.sleep_ms(5000)
