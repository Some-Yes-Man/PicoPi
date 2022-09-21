from machine import Pin
from utime import sleep, sleep_ms

import ferdi.src.MORSE_DICT
from ferdi.src import MORSE_DICT


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
    inputPin -> its the input pin, silly!
    oneDuration -> duration in [ms] defines short and blank, long is 2* short
    scanInterval -> defines the fraction of the short in which the pin is scanned, kind of controls the accuracy

    transforms received Light-input into text, based on short-duration
    """
    def morseReceive(self, oneDuration, inputPin, scanInterval):
        received = []
        scan = oneDuration/scanInterval
        print('scan '+str(scan))
        curTail = []
        window = []
        while not self.terminationSend(curTail, (4*scanInterval)):
            cur = inputPin.value()
            print('0')
            window.append(cur)
            curTail.append(cur)
            print('window '+str(window))
            print('tail '+str(curTail))
            if len(window) == (2*scanInterval):
                print('1')
                received.extend(self.guessWhat(window))
                window = []
            if len(curTail) > (4*scanInterval):
                print('2')
                curTail.remove(0)
            sleep_ms(1000-int(scan))
        return received


    def mapInputToMorseInput(self, input):
        result = []
        return result


    """
    . -> short
    - -> long
    _ -> blank
    
    uses the already defined and split input to create the text of the received morse  
    """
    def morseToText(self, input):
        text = ""
        curWord = ""
        letter = []
        blankHit = False
        print(input)
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


    def terminationSend(self, tail, size):
        if len(tail) == size:
            if 0 in tail:
                return True
        return False

    def guessWhat(self, window):
        print("guess "+str(window))
        cur = []
        changed = True
        if '1' in window:
            for i in range(len(window)):
                if not window[i] == 0:
                    if changed:
                        cur.append(window[i])
                    else:
                        changed = True
                    #new letter, word or space beings

                    if not window[i] == 0:
                        return True

            if window.count(1) > window.count(0):
                return ["-"]
            else:
                halfSizePlusOne = (len(window)/2)+1
                if window[0:halfSizePlusOne].count(1)>((halfSizePlusOne/2)+1):
                    return [".","-"]
                else:
                    return ["_","."]
        return ["_", "_"]

