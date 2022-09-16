import includes.constants as const
from includes.oled import OLED
import time

const.getPWM(13)
const.getPWM(14)
const.getPWM(15)

print("Turning off pins")
for pin in const.pins:
  if pin != None:
    pin.value(0)
time.sleep(1)


print("Turning off pwm")
for pwm in const.pwms:
  if pwm != None:
    pwm.duty_u16(0)
    #pwm.freq(10)
    #pwm.deinit()
time.sleep(1)


oled = OLED()
oled.fill(0)
