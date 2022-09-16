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
    }

    def __toMorseCode(self, string, codeMap):
        letters = list(string)
        output = ""
        letterCount = len(letters)
        for letterIndex in range(letterCount):
            letter = letters[letterIndex].lower()
            if letter in codeMap:
                output += codeMap[letter]
                if letterIndex < letterCount - 1:
                    output += codeMap[self.__separatorKey]
            else:
                return KeyError
        return output

    def toAcustic(self, string):
        return self.__toMorseCode(string, Morse.__acustic)

    def toBlink(self, string):
        return self.__toMorseCode(string, self.__blinking)

    def __toStringFromCode(self, morse, codeMap):
        words = morse.split(
            codeMap[self.__separatorKey] + codeMap[" "] + codeMap[self.__separatorKey]
        )
        output = ""

        for word in words:
            letters = word.split(codeMap[self.__separatorKey])
            for letter in letters:
                for string, code in codeMap.items():
                    if letter == code:
                        output += string
            output += " "
        return output[:-1]

    def toStringFromAcustic(self, morse):
        return self.__toStringFromCode(morse, self.__acustic)

    def toStringFromBlink(self, morse):
        return self.__toStringFromCode(morse, self.__blinking)
