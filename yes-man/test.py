import time
from machine import Timer

syncPattern = [1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1]
iterationIndex = -1
symbolIndex = -1
symbol = None
symbolCounts = []

for patternIndex in range(len(syncPattern)):
    if (syncPattern[patternIndex] != symbol):
        symbolIndex = (symbolIndex + 1) % 2
        symbolCounts.append(1)
        if (symbolIndex == 0):
            iterationIndex += 1
        symbol = syncPattern[patternIndex]
    else:
        symbolCounts[iterationIndex * 2 + symbolIndex] += 1

print(symbolCounts)


def printHello(timer):
    foo = 2/5
    print("Hello: " + str(foo))


def printWorld(timer):
    bar = 5/3
    print("World: " + str(bar))


timer1 = Timer()
timer1.init(period=523, mode=Timer.PERIODIC, callback=printHello)
timer2 = Timer()
timer2.init(period=421, mode=Timer.PERIODIC, callback=printWorld)

counter = 0
while True:
    counter += 1
    print("Bob: " + str(counter / 11))
    time.sleep_ms(50)
