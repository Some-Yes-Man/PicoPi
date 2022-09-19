from machine import Timer

class lightSensor:

    def __init__(self, pin):
        self.pin = pin
        self.pollingState = True
        self.pin.irq(lambda t: self.syncForMorse() if self.pollingState == True else print("ignored interrupt"))

    def syncForMorse(self):
        self.pollingState = False
        received = []
        t1 = Timer(1)
        t1.init(period=5000, mode=Timer.PERIODIC, callback=lambda t: received.append(self.pin.value))

        #Todo: Timer is over - return 1?
        if received.__len__() > 7:
            return 1
