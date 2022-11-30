class Morse:
    __separatorKey = "#sep#"
    __acustic = {
        "0": "-----",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
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
        ".": ".-.-.-",
        ",": "--..--",
        "?": "..--..",
        "!": "-.-.--",
        "-": "-....-",
        "/": "-..-.",
        "@": ".--.-.",
        "(": "-.--.",
        ")": "-.--.-",
        " ": " ",
        __separatorKey: " ",
    }
    __blinking = {
        "0": "### ### ### ### ###",
        "1": "# ### ### ### ###",
        "2": "# # ### ### ###",
        "3": "# # # ### ###",
        "4": "# # # # ###",
        "5": "# # # # #",
        "6": "### # # # #",
        "7": "### ### # # #",
        "8": "### ### ### # #",
        "9": "### ### ### ### #",
        "a": "# ###",
        "b": "### # # #",
        "c": "### # ### #",
        "d": "### # #",
        "e": "#",
        "f": "# # ### #",
        "g": "### ### #",
        "h": "# # # #",
        "i": "# #",
        "j": "# ### ### ###",
        "k": "### # ###",
        "l": "# ### # #",
        "m": "### ###",
        "n": "### #",
        "o": "### ### ###",
        "p": "# ### ### #",
        "q": "### ### # ###",
        "r": "# ### #",
        "s": "# # #",
        "t": "###",
        "u": "# # ###",
        "v": "# # # ###",
        "w": "# ### ###",
        "x": "### # # ###",
        "y": "### # ### ###",
        "z": "### ### # #",
        ".": "# ### # ### # ###",
        ",": "### ### # # ### ###",
        "?": "# # ### ### # #",
        "!": "### # ### # ### ###",
        "-": "### # # # # ###",
        "/": "### # # ### #",
        "@": "# ### ### # ### #",
        "(": "### # ### ### #",
        ")": "### # ### ### # ###",
        " ": " ",
        __separatorKey: "   ",
        "^": "# # # # # "
    }

    @classmethod
    def __toMorseCode(cls, string, codeMap):
        letters = list(string)
        output = ""
        letterCount = len(letters)
        for letterIndex in range(letterCount):
            letter = letters[letterIndex].lower()
            if (letter in codeMap):
                output += codeMap[letter]
                if (letterIndex < letterCount - 1):
                    output += codeMap[Morse.__separatorKey]
            else:
                return KeyError
        return output

    @classmethod
    def toAcustic(cls, string):
        return Morse.__toMorseCode(string, Morse.__acustic)

    @classmethod
    def toBlink(cls, string):
        return Morse.__toMorseCode(string, Morse.__blinking)

    @classmethod
    def __toStringFromCode(cls, morse, codeMap):
        words = morse.split(codeMap[Morse.__separatorKey] + codeMap[" "] + codeMap[Morse.__separatorKey])
        output = ""

        for word in words:
            output += Morse.__toWordFromCode(word, codeMap) + " "
        return output[:-1]

    @classmethod
    def __toWordFromCode(cls, morseWord, codeMap):
        letters = morseWord.split(codeMap[Morse.__separatorKey])
        output = ""
        for letter in letters:
            output += Morse.__toLetterFromCode(letter, codeMap)
        return output

    @classmethod
    def __toLetterFromCode(cls, morseLetter, codeMap):
        for string, code in codeMap.items():
            if (morseLetter == code):
                return string
        return "#"

    @classmethod
    def toStringFromAcustic(cls, morse):
        return Morse.__toStringFromCode(morse, Morse.__acustic)

    @classmethod
    def toWordFromAcustic(cls, morse):
        return Morse.__toWordFromCode(morse, Morse.__acustic)

    @classmethod
    def toLetterFromAcustic(cls, morse):
        return Morse.__toLetterFromCode(morse, Morse.__acustic)

    @classmethod
    def toStringFromBlink(cls, morse):
        return Morse.__toStringFromCode(morse, Morse.__blinking)

    @classmethod
    def toWordFromBlink(cls, morse):
        return Morse.__toWordFromCode(morse, Morse.__blinking)

    @classmethod
    def toLetterFromBlink(cls, morse):
        return Morse.__toLetterFromCode(morse, Morse.__blinking)
