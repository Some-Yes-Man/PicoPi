import includes.constants as const
from machine import Timer
from time import sleep

def blinkLED(timer):
    const.ONBOARD_LED.toggle()

timerLED = Timer()
timerLED.init(freq=10, mode=Timer.PERIODIC, callback=blinkLED)


while True:
    for duty in range(200):
        sleep(10.01)
