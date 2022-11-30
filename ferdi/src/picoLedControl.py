from machine import Pin
from utime import sleep, sleep_ms

from ferdi.src import MORSE_DICT
import uasyncio

class picoLedControl:

    def __init__(self, baseState, pin):
        self.baseState = baseState
        self.pin = pin
        self.pin.value(baseState)


    def turnOn(self):
        self.pin.value(1)

    def turnOff(self):
        self.pin.value(0)

    def blink(self, duration, pause):
        counter = 0
        while counter < duration:
            self.turnOn()
            sleep(pause)
            self.turnOff()
            sleep(pause)
            counter = counter + 1

    """
    shortLongTuple -> defines the duration for _short and for _long in [ms]
    pause -> break between letters, twice for words in [ms]
    
    controls this LED-pin to morse given text based on tuple-information 
    """
    async def morseSend(self, text, pause, pin):
        words = self.splitText(text)
        await uasyncio.sleep_ms(100)
        for word in words.__await__():
            for w in word:
                if w == '.':
                    pin.value(0)
                    sleep_ms(pause)
                    pin.value(1)
                    sleep_ms(pause)
                if w == '-':
                    pin.value(0)
                    sleep_ms(pause)
                    sleep_ms(pause)
                    pin.value(1)
                    sleep_ms(pause)
                else:
                    pin.value(1)
                    sleep_ms(pause)
            pin.value(1)
            sleep_ms(pause)
            pin.value(1)
        return

    async def splitText(self, text):
        words = []
        cur = ""
        for s in list(text):
            if s.isspace():
                words.append(cur)
                cur = ""
            else:
                temp = MORSE_DICT.MORSE_CODE_DICT[s.upper()]
                cur = cur + temp + "_"
        if cur == "":
            return words
        else:
            words.append(cur)
            return words

    """
    inputPin -> its the input pin, silly!
    oneDuration -> duration in [ms] defines short and blank, long is 2* short
    scanInterval -> defines the fraction of the short in which the pin is scanned, kind of controls the accuracy

    transforms received Light-input into text, based on short-duration
    """
    def morseReceive(self, inputPin, scanInterval, oneDuration=50):
        received = []
        oneDuration = oneDuration if 100 > oneDuration > 10 else 50
        scan = oneDuration/scanInterval
        curTail = []
        window = []
        # Todo: should probably test if this actually works lol !
        while not self.terminationSend(curTail, (4*scanInterval)):
            cur = inputPin.value()
            print('0')
            window.append(cur)
            curTail.append(cur)
            if len(window) == (2*scanInterval):
                received.extend(self.guessWhat(window))
                window = []
            if len(curTail) > (4*scanInterval):
                curTail.remove(0)
            sleep_ms(1000-int(scan))
        return received

    """
    . -> short
    - -> long
    _ -> blank
    
    uses the already defined and split input to create the text of the received morse  
    """
    async def morseToText(self, input):
        text = word = letter = ""
        newLetter = newWord = False
        for x in input:
            if x == "_":
                if newLetter:
                    if not newWord:
                        newWord = True
                else:
                    newLetter = True
            else:
                if newLetter:
                    for key, value in MORSE_DICT.MORSE_CODE_DICT.items():
                        if letter == value:
                            word = word + key
                    letter = x
                    newLetter = False
                else:
                    letter = letter + x
                if newWord:
                    text = text + word
                    word = " "
                    newWord = False
        if not letter == "":
            for key, value in MORSE_DICT.MORSE_CODE_DICT.items():
                if letter == value:
                    word = word + key
        if not word == "":
            text = text + word
        return text


    def terminationSend(self, tail, size):
        if len(tail) == size:
            if 0 in tail:
                return True
        return False

    def guessWhat(self, window):
        if 1 in window:
            if window.count(1) > window.count(0):
                return ["-"]
            else:
                halfSizePlusOne = int((len(window)/2)+1)
                if window[0:halfSizePlusOne].count(1)>((halfSizePlusOne/2)+1):
                    return [".","-"]
                else:
                    return ["_","."]
        return ["_", "_"]

