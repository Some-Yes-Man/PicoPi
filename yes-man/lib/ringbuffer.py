class RingBuffer:

    __readIndex = 0
    __writeIndex = 0
    __bufferSize = 0
    __empty = True

    def __init__(self, size):
        if (size <= 0):
            raise ValueError("RingBuffer must at least be of size 1.")
        self.__bufferSize = size
        self.__bufferArray = bytearray(self.__bufferSize)

    def write(self, byte):
        if (not self.__empty and (self.__writeIndex == self.__readIndex)):
            raise OverflowError("RingBuffer overflow!")
        self.__bufferArray[self.__writeIndex] = byte
        self.__writeIndex = (self.__writeIndex + 1) % len(self.__bufferArray)
        self.__empty = False

    def isEmpty(self):
        return self.__empty

    def read(self):
        if (self.__empty):
            return None
        tmp = self.__bufferArray[self.__readIndex]
        self.__readIndex = (self.__readIndex + 1) % self.__bufferSize
        if (self.__readIndex == self.__writeIndex):
            self.__empty = True
        return tmp
