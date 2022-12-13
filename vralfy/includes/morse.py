# https://morsedecoder.com/de/
class Morse():
  def __init__(self):
    self.dit = '.'
    self.dah = '-'
    self.pause = ' '
    self.binary_high = '='
    self.binary_low = '.'
    self.signal = {
      "start": "ka",
      "end": "ar",
      "pause": "bt",
      "confirm": "ve",
      "end_transmission": "sk",
      "error": "eeeee e e e",
    }
    self.alphabet={
      # Letters
      "a": ".-",
      "b": "-...",
      "c": "-.-.",
      "d": "-..",
      "e": ".",
      "f": "..-.",
      "g": "--.",
      "h": "....",
      "i": "..",
      "j": ".---",
      "k": "-.-",
      "l": ".-..",
      "m": "--",
      "n": "-.",
      "o": "---",
      "p": ".--.",
      "q": "--.-",
      "r": ".-.",
      "s": "...",
      "t": "-",
      "u": "..-",
      "v": "...-",
      "w": ".--",
      "x": "-..-",
      "y": "-.--",
      "z": "--..",
      # Umlaute
      "ä": ".-.-",
      "ö": "---.",
      "ü": "..--",
      "ß": "......",
      # Numbers
      "1": ".----",
      "2": "..---",
      "3": "...--",
      "4": "....-",
      "5": ".....",
      "6": "-....",
      "7": "--...",
      "8": "---..",
      "9": "----.",
      "0": "-----",
      #
      " ": "",
      ".": ".-.-.-",
      ",": "--..--",
      "?": "..--..",
      "'": ".----.",
      "!": "-.-.--",
      "/": "-..-.",
      "(": "-.--.",
      ")": "-.--.-",
      "&": ".-...",
      ":": "---...",
      ";": "-.-.-.",
      "=": "-...-",
      "+": ".-.-.",
      "-": "-....-",
      "_": "..--.-",
      "\"": ".-..-.",
      "$": "...-..-",
      "@": ".--.-.",
      "¿": "..-.-",
      "¡": "--...-",
    }

  def signal_start(self):
    return self.textToMorse(self.signal['start'])

  def signal_end(self):
    return self.textToMorse(self.signal['end'])

  def signal_pause(self):
    return self.textToMorse(self.signal['pause'])

  def signal_confirm(self):
    return self.textToMorse(self.signal['confirm'])

  def signal_end_transmission(self):
    return self.textToMorse(self.signal['end_transmission'])

  def signal_error(self):
    return self.toMorse(self.signal['error'])

  def textToMorse(self, text, dit = None, dah = None, pause = None):
    if dit == None: dit = self.dit
    if dah == None: dah = self.dah
    if pause == None: pause = self.pause

    ret = ""
    for c in text.lower():
      if c in self.alphabet.keys():
        for d in self.alphabet[c]:
          if d == '.': ret += dit
          if d == '-': ret += dah
        ret += pause
    return ret

  def textToBinary(self, text, dit = None, dah = None, pause = None, high = None, low = None):
    return self.morseToBinary(self.textToMorse(text, dit, dah, pause), dit, dah, pause , high, low)

  def morseToBinary(self, morse, dit = None, dah = None, pause = None, high = None, low = None):
    if dit == None: dit = self.dit
    if dah == None: dah = self.dah
    if pause == None: pause = self.pause
    if high == None: high = self.binary_high
    if low == None: low = self.binary_low

    ret = ""
    for c in morse:
      if c == dit: ret += high + low
      elif c == dah: ret += high * 3 + low
      elif c == pause: ret += low * 2
    return ret

  def morseToText(self, morse, dit = None, dah = None, pause = None):
    if dit == None: dit = self.dit
    if dah == None: dah = self.dah
    if pause == None: pause = self.pause

    ret = ''
    letters = morse.split(pause)
    for letter in letters:
      if letter == '': ret += ' '
      else:
        list = [''] * len(letter)
        for i in range(len(letter)):
          if letter[i] == dit: list[i]='.'
          elif letter[i] == dah: list[i]='-'
        ret += [k for k, v in self.alphabet.items() if v == ''.join(list)][0]
    return ret

  def binaryToText(self, binary, dit = None, dah = None, pause = None, high = None, low = None):
    return self.morseToText(self.binaryToMorse(binary, dit, dah, pause, high, low), dit, dah, pause)

  def binaryToMorse(self, binary, dit = None, dah = None, pause = None, high = None, low = None):
    if dit == None: dit = self.dit
    if dah == None: dah = self.dah
    if pause == None: pause = self.pause
    if high == None: high = self.binary_high
    if low == None: low = self.binary_low

    ret = ""
    while len(binary) > 0:
      if binary.startswith(high + low):
        ret += dit
        binary = binary[2:]
      elif binary.startswith(high*3+low):
        ret += dah
        binary = binary[4:]
      elif binary.startswith(low*2):
        ret += pause
        binary = binary[2:]
      else:
        binary = binary[1:]
    return ret

  def transmitText(self, text, callback = None):
    self.transmitBinary(self.textToBinary(text, high="1", low='0'), callback=callback)

  def transmitMorse(self, morse, callback = None):
    self.transmitBinary(self.morseToBinary(morse, high="1", low='0'), callback=callback)

  def transmitBinary(self, binary, callback = None):
    if callback == None: return
    for v in binary: callback(v=='1' if 1 else 0)

if __name__ == "__main__":
  coder = Morse()
  text = "abcdefghijklmopqrstuvwxyz"
  text = "hello"
  print(text)
  print(coder.textToMorse(text))
  for letter in text:
    print(letter + ':'
          + '\t' + coder.textToMorse(letter)
          + '\t' + coder.textToBinary(letter)
          )