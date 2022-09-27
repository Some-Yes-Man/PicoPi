
"""
    Testing without pico being connected
"""
from machine import Pin
from utime import sleep

from ferdi.src.picoLedControl import picoLedControl

dataPin = Pin(22, Pin.IN)
ledPin = Pin('LED', Pin.OUT)
pL = picoLedControl(0, dataPin)
# #a aaabb bb
input = ".-___.-__.-__.-__-...__-...___-...___-..."
out = pL.morseToText(input)
print("out "+str(out))
# print()
# sleep(1)
#pL.pin = ledPin
#pL.morseSend("Hello You ", 0.5)
#print()
#sleep(1)
#pL.pin = dataPin
# received = [1, 0, 1, 0, 1, 0, 1, 0]
# if received == [1, 0, 1, 0, 1, 0, 1] or received == [0, 1, 0, 1, 0, 1, 0]:
#     print('true')
# windows = [[0, 0, 1, 0,1],[1, 1, 1, 0,0],[0, 0, 1, 0,0],[1, 1, 1, 1,1],[0, 0, 0,1, 1],[0, 1, 1, 0]]
#
# print("windows:")
# for window in windows:
#     print(pL.guessWhat(window))


