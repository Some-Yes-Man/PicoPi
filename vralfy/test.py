from includes.huffman import Huffman
from includes.morse import Morse

h = Huffman()
m = Morse()
text = "abcdefghijklmopqrstuvwxyz"
text = "hello"
print(text)
print(m.textToMorse(text))
print(h.textToBinary(text, high='1', low='0'))
for letter in text:
  print(letter + ':'
        + '\t' + m.textToMorse(letter)
        + '\t' + m.textToBinary(letter)
        + '\t' + h.textToMorse(letter)
        + '\t' + h.textToBinary(letter)
        )