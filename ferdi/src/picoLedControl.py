from machine import Pin
from utime import sleep

import MORSE_DICT


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
    def morseSend(self, text, pause, shortLongTuple):
        words = self.splitText(text)
        for word in words:
            for w in word:
                if w == '.':
                    self.turnOn()
                    sleep(shortLongTuple[0])
                    self.turnOff()
                    sleep(pause)
                else:
                    self.turnOn()
                    sleep(shortLongTuple[1])
                    self.turnOff()
                    sleep(pause)
            sleep(pause)
            sleep(pause)
            self.sendMorseTermination(pause)


    def sendMorseTermination(self, pause):
        for i in range(5):
            self.turnOn()
            sleep(pause)
            self.turnOff()
            sleep(pause)


    def splitText(self, text):
        words = []
        cur = ''
        for s in list(text):
            if s.isspace():
                words.append(cur)
            else:
                cur.__add__(MORSE_DICT.MORSE_CODE_DICT[s.upper()])
        return words

    """
    shortLongTuple -> defines the duration for _short and for _long in [ms]
    pause -> break between letters, twice for words in [ms]

    transforms received Light-input into text based on shortLongTuple and base definition
    """
    def morseReceive(self, onDuration, inputPin):
        received = []
        scan = onDuration/2
        curTail = []
        pre = ""
        while not self.terminationSend(curTail):
            cur = inputPin.value()
            if cur == "off":
                received.append("_")
            if cur == "on":
                if pre == "on":
                    received.append("_")
                else:
                    received.append(".")
            pre = cur

            # Todo: tail als sliding window -> mapping tail to symbols

            curTail.append(cur)
            if curTail.__len__() > 4:
                curTail.remove(0)
            sleep(1-scan)
        data = received.__len__()-(curTail.__len__()-1)
        return received[0:data]


    def mapInputToMorseInput(self, input):
        result = []
        return result


    """
    uses the already defined and split input to create the text of the received morse  
    . -> short
    - -> long
    _ -> blank
    """
    def morseToText(self, input):
        text = ""
        curWord = ""
        letter = []
        blankHit = False
        for x in input:
            if x == "_":
                if blankHit:
                    letter.append(" ")
                    blankHit = False
                else:
                    letter.append(curWord)
                    curWord = ""
                    blankHit = True
            else:
                curWord = curWord+x
                blankHit = False
        letter.append(curWord)
        for l in letter:
            if l.isspace():
                text = text + " "
            else:
                for key, value in MORSE_DICT.MORSE_CODE_DICT.items():
                    if l == value:
                        text = text + key
        return text


    def terminationSend(self, tail):
        finalSignal = ["1","0","1","0"]
        if tail == finalSignal:
            return True
        return False

