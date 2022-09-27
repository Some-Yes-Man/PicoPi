from machine import Pin
from utime import sleep, sleep_ms

import ferdi.src.MORSE_DICT
from ferdi.src import MORSE_DICT


class picoLedControl:

    def __init__(self, baseState, pinId, pinState):
        self.baseState = baseState
        self.pin = Pin(pinId, pinState)
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
    def morseSend(self, text, pause, pin):
        sleep_ms(pause)
        sleep_ms(pause)
        words = self.splitText(text)
        for word in words:
            for w in word:
                print(w)
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
                    sleep_ms(pause)
                print("here")
            sleep_ms(pause)
            sleep_ms(pause)
            self.sendMorseTermination(pause)
        return


    def sendMorseTermination(self, pause):
        for i in range(5):
            self.turnOn()
            sleep(pause)
            self.turnOff()
            sleep(pause)


    def splitText(self, text):
        words = []
        cur = ""
        for s in list(text):
            if s.isspace():
                words.append(cur)
                cur = ""
            else:
                temp = MORSE_DICT.MORSE_CODE_DICT[s.upper()]
                cur = cur + temp + "_"
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
        curTail = []
        window = []
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
        letter = ""
        newSymbol = False
        newLetter = False
        newWord = False

#        ".-___.-__.-__.-__-.._.__-._..___-...___-..."

        for x in input:
            print("the x "+str(x))
            if x == "_":
                if newSymbol:
                    if newLetter:
                        if newWord:
                            curWord = curWord+" "
                        else:
                            newWord = True
                    else:
                        newLetter = True
                else:
                    newSymbol = True
            else:
                if newSymbol:
                    for key, value in MORSE_DICT.MORSE_CODE_DICT.items():
                        if letter == value:
                            curWord = curWord + key
                            letter = ""
                else:
                    letter = letter + x
                if newLetter:
                    #curWord = curWord + letter
                    letter = x
                if newWord:
                    print("cur ["+ str(curWord) + "]")
                    text = text + curWord
                    curWord = ""
                    newSymbol = False
                    newWord = False
                    newLetter = False




            print("bools " + str(newSymbol) +", "+str(newLetter)+", "+str(newWord))
            print("letter "+str(letter))
            print("curWord "+str(curWord))
            print("text "+str(text))
            print()
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

