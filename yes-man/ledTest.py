from lib.led import Led
from lib.morse import Morse
from lib.sensor import Sensor

m = Morse()
l = Led(0, 10)
#s = LightSensor(28)

l.blink(m.toBlink("sos sos sos sos"))
