import includes.constants as const
from includes.huffman import Huffman
from includes.morse import Morse
from includes.oled import OLED
import time
import uasyncio
from machine import Pin

bautrate  = 0.05
control_signals = False

morse=Morse()
huffman=Huffman()
translator = morse

messages = [
  'SOS',
  'Hello World!',
  # '   '*5,
  ('e'*3 + 'T') * 4
]
messageIndex = 0
messageBuffer = ""

oled=OLED(i2cPosition=5)
pwm_speaker = const.getPWM(13)
pwm_led = const.getPWM(14)
led = const.ONBOARD_LED

pwm_speaker.freq(600)
pwm_speaker.duty_u16(0)
pwm_led.duty_u16(0)

def signal(v):
  led.value(v)
  pwm_led.duty_u16(v * 40000)
  pwm_speaker.duty_u16(v * 2000)
  time.sleep(bautrate)

async def transmit():
  global messageBuffer
  while True:
    if len(messageBuffer) > 0:
      print("Transmitting ")
      print("Message: " + messageBuffer)
      print("Morse:   " + morse.textToMorse(messageBuffer))
      print("         " + morse.textToMorse(messageBuffer, dit="dit ", dah = "dah ", pause="_ "))
      print("Huffman: " + huffman.textToMorse(messageBuffer))
      print("Binary:  " + translator.textToBinary(messageBuffer))
      print("Reverse: " + translator.morseToText(translator.textToMorse(messageBuffer)))
      print("Reverse: " + translator.binaryToText(translator.textToBinary(messageBuffer)))

      if control_signals:
        oled.fill_rect(0, 36, 200, 50, 0)
        oled.text("START = " + translator.signal_start(), 0, 36)
        oled.show()
        translator.transmitMorse(translator.signal_start(), signal)

      while len(messageBuffer) > 0:
        oled.fill(0)
        oled.text(messageBuffer, 0, 0)
        oled.show()
        char = messageBuffer[0]
        morseMessage = translator.textToMorse(char)
        oled.fill_rect(0, 36, 200, 50, 0)
        oled.text(char + " = " + morseMessage, 20, 36)
        oled.show()
        translator.transmitText(char, signal)
        messageBuffer = messageBuffer[1:]

      if control_signals:
        oled.fill_rect(0, 36, 200, 50, 0)
        oled.text("END = " + translator.signal_end(), 0, 36)
        oled.show()
        translator.transmitMorse(translator.signal_end(), signal)

    oled.fill(0)
    oled.text("DONE", 45, 25)
    oled.show()
    await uasyncio.sleep(bautrate*5)

def irqButton(pin):
  global messages
  global messageIndex
  global messageBuffer
  messageBuffer += " " + messages[messageIndex];
  messageIndex = (messageIndex + 1) % len(messages)
  print(messageBuffer)

def irqSensor(pin):
  if pin.value() == 0:
    print('UP')
  elif pin.value() == 1:
    print('DOWN')

async def main():
    oled.text('press da button', 0, 40)
    oled.show()

    const.setIrq(12, handler=irqButton) # Button
    const.setIrq(18, handler=irqSensor, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING) # Lightsensor
    await uasyncio.create_task(transmit())
    while True:
        uasyncio.sleep(2)

uasyncio.run(main())
