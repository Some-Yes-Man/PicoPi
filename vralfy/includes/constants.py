from machine import Pin, PWM, ADC

pins = [None] * 28        # 28 Possible GPIO Pins
pwms = [None] * len(pins) # PWM for each PIN

def getPin(gpio, write = False):
  if pins[gpio] == None:
    pins[gpio] = Pin(gpio, write if Pin.OUT else Pin.IN)
  return pins[gpio]

def setIrq(gpio, handler = None, trigger = Pin.IRQ_RISING, priority = 1, hard = False):
  pin = getPin(gpio, False)
  return pin.irq(handler=handler, trigger=trigger)

def getPWM(gpio):
  if (pwms[gpio] == None):
    pwms[gpio] = PWM(getPin(gpio, True))
    pwms[gpio].freq(440)
  return pwms[gpio]

# Aliases
def getI2C0(pos):
  if pos < 0 or pos > 5: return [None, None]
  return [getPin(pos * 4), getPin(pos*4+1)]

def getI2C1(pos): # there is anotherone at SDA=26 and SCL=27
  if pos < 0 or pos > 4: return [None, None]
  return [getPin(2 + pos * 4), getPin(2 + pos*4+1)]

def getADC(pos):
  if pos < 0 or pos > 2: return None
  return ADC(26 + pos)


ONBOARD_LED=Pin("LED", Pin.OUT)

if __name__ == "__main__":
  from time import sleep
  while True:
    ONBOARD_LED.toggle()
    sleep(0.5)