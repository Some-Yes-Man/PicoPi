from lib.led import Led
from lib.morse import Morse
from lib.sensor import LightSensor

m = Morse()
l = Led(0, 40)
#s = LightSensor(28)

l.blink(m.toBlink("norbert rocks poergpoihop weohw fiugiluwf   wef"))
