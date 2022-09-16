from lib.morse import Morse

m = Morse()
alphabet = "qwertzuiopasdfghjklyxcvbnm,.-!?()@ /"

assert m.toAcustic(alphabet) == "--.- .-- . .-. - --.. ..- .. --- .--. .- ... -.. ..-. --. .... .--- -.- .-.. -.-- -..- -.-. ...- -... -. -- --..-- .-.-.- -....- -.-.-- ..--.. -.--. -.--.- .--.-.   -..-."
assert m.toStringFromAcustic(m.toAcustic(alphabet)) == alphabet

assert m.toBlink(alphabet) == "### ### # ###   # ### ###   #   # ### #   ###   ### ### # #   # # ###   # #   ### ### ###   # ### ### #   # ###   # # #   ### # #   # # ### #   ### ### #   # # # #   # ### ### ###   ### # ###   # ### # #   ### # ### ###   ### # # ###   ### # ### #   # # # ###   ### # # #   ### #   ### ###   ### ### # # ### ###   # ### # ### # ###   ### # # # # ###   ### # ### # ### ###   # # ### ### # #   ### # ### ### #   ### # ### ### # ###   # ### ### # ### #       ### # # ### #"
assert m.toStringFromBlink(m.toBlink(alphabet)) == alphabet
