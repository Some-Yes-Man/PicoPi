from lib.ringbuffer import RingBuffer

try:
    RingBuffer(0)
except ValueError:
    pass
else:
    assert False, "RingBuffer creation with insufficient size should throw ValueError."

try:
    miniBuffer = RingBuffer(1)
    miniBuffer.write(42)
    assert miniBuffer.read() == 42, "RingBuffer of size 1 works as expected."
    miniBuffer.write(105)
    assert miniBuffer.read() == 105, "RingBuffer of size 1 works as expected."
except ValueError:
    assert False, "RingBuffer of size 1 is valid."

rBuffer = RingBuffer(10)

assert rBuffer.isEmpty(), "New RingBuffer should say it's empty."

assert rBuffer.read() is None, "New RingBuffer should return 'None' on read()."

rBuffer.write(1)

assert not rBuffer.isEmpty(), "New RingBuffer after single write() should not be empty."

assert rBuffer.read() == 1, "New RingBuffer after single write() should return value on read()."

assert rBuffer.isEmpty(), "New RingBuffer after single write/read combo should be empty again."

for i in range(2, 5):
    rBuffer.write(i)

assert not rBuffer.isEmpty(), "Empty RingBuffer after multiple writes should not be empty."

for i in range(2, 5):
    assert rBuffer.read() == i, "RingBuffer after multiple writes should return values in same order."

assert rBuffer.isEmpty(), "RingBuffer, after multiple writes and reading to end, should be empty again."

for i in range(6, 14):
    rBuffer.write(i)
for i in range(6, 14):
    assert rBuffer.read() == i, "RingBuffer, after multiple writes surpassing the end of the ring, should return values in same order."

assert rBuffer.isEmpty(), "RingBuffer, after multiple writes and reading over the end, should be empty again."

try:
    for i in range(1, 12):
        rBuffer.write(i)
except OverflowError:
    pass
else:
    assert False, "Overflown RingBuffer with insufficient size should throw OverflowError."

print("RingBuffer tests done.")
