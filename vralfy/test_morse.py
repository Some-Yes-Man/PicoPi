import includes.constants as const
from includes.huffman import Huffman
from includes.morse import Morse
from includes.oled import OLED
import time

bautrate  = 0.05
control_signals = False

morse=Morse()
huffman=Huffman()
translator = morse

oled=OLED(i2cPosition=5)
pwm_speaker = const.getPWM(13)
pwm_led = const.getPWM(14)
led = const.ONBOARD_LED
lightsensor = const.getPin(18)

pwm_speaker.freq(600)
pwm_speaker.duty_u16(0)
pwm_led.duty_u16(0)

def signal(v):
  led.value(v)
  pwm_led.duty_u16(v * 40000)
  pwm_speaker.duty_u16(v * 2000)
  time.sleep(bautrate)

def transmit(plainMessage):
  print("Transmitting ")
  print("Message: " + plainMessage)
  print("Morse:   " + morse.textToMorse(plainMessage))
  print("         " + morse.textToMorse(plainMessage, dit="dit ", dah = "dah ", pause="_ "))
  print("Huffman: " + huffman.textToMorse(plainMessage))
  print("Binary:  " + translator.textToBinary(plainMessage))
  print("Reverse: " + translator.morseToText(translator.textToMorse(plainMessage)))
  print("Reverse: " + translator.binaryToText(translator.textToBinary(plainMessage)))
  oled.fill(0)
  oled.text(plainMessage, 0, 0)
  oled.show()

  if control_signals:
    oled.fill_rect(0, 36, 200, 50, 0)
    oled.text("START = " + translator.signal_start(), 0, 36)
    oled.show()
    translator.transmitMorse(translator.signal_start(), signal)

  for char in plainMessage:
    morseMessage = translator.textToMorse(char)
    oled.fill_rect(0, 36, 200, 50, 0)
    oled.text(char + " = " + morseMessage, 20, 36)
    oled.show()
    translator.transmitText(char, signal)

  if control_signals:
    oled.fill_rect(0, 36, 200, 50, 0)
    oled.text("END = " + translator.signal_end(), 0, 36)
    oled.show()
    translator.transmitMorse(translator.signal_end(), signal)

messages = [
  'SOS',
  'Hello World!',
  # '   '*5,
  ('e'*3 + 'T') * 4
]
messageIndex = 0

def irqCallback(pin):
  global messages
  global messageIndex
  transmit(messages[messageIndex])
  messageIndex = (messageIndex + 1) % len(messages)
  oled.fill(0)
  oled.text("DONE", 45, 25)
  oled.show()

oled.text('press da button', 0, 40)
oled.show()
const.setIrq(12, handler=irqCallback)

while True:
  time.sleep(0.2)