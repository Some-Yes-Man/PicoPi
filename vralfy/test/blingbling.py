import includes.constants as const
from includes.oled import OLED
from includes.sensors import Sensors

from machine import Timer
from time import sleep

PWM13 = const.getPWM(25)
PWM14 = const.getPWM(14)

import reset

oled = OLED()
sensors = Sensors()

def blinkLED(timer):
    const.ONBOARD_LED.toggle()

def printOled(timer):
    oled.fill(0)
    oled.blit(OLED.buffer_raspberry, 96, 0)
    # Add some text
    oled.text(str(round(sensors.getADC(),2)),40,8)
    oled.text("Hello", 0, 16)
    oled.show()

printOled(None)

timerLED = Timer()
timerOLED = Timer()
timerOLED.init(freq=0.5, mode=Timer.PERIODIC, callback=printOled)
timerLED.init(freq=10, mode=Timer.PERIODIC, callback=blinkLED)


PWM13.freq(1000)
PWM14.freq(1000)

while True:
    for duty in range(200):
        PWM14.duty_u16(duty*300 % 6000)
        sleep(0.01)
        oled.text("-", duty % 100, 24)
        oled.show()