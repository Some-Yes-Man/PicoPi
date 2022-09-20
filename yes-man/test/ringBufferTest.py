from lib.ringbuffer import RingBuffer

r = RingBuffer(10)

assert r.isEmpty(), "New RingBuffer should say it's empty."

assert r.read() is None, "New RingBuffer should return 'None' on read()."

r.write(1)

assert not r.isEmpty(), "New RingBuffer after single write() should not be empty."

assert r.read() == 1, "New RingBuffer after single write() should return value on read()."

assert r.isEmpty(), "New RingBuffer after single write/read combo should be empty again."

for i in range(2, 5):
    r.write(i)

assert not r.isEmpty(), "Empty RingBuffer after multiple writes should not be empty."

for i in range(2, 5):
    assert r.read() == i, "RingBuffer after multiple writes should return values in same order."

assert r.isEmpty(), "RingBuffer, after multiple writes and reading to end, should be empty again."

for i in range(6, 14):
    r.write(i)
for i in range(6, 14):
    assert r.read() == i, "RingBuffer, after multiple writes surpassing the end of the ring, should return values in same order."

assert r.isEmpty(), "RingBuffer, after multiple writes and reading over the end, should be empty again."

try:
    for i in range(1, 12):
        r.write(i)
except OverflowError:
    pass
else:
    assert False, "RingBuffer, with insufficient size should throw OverflowError."

print("RingBuffer tests done.")
