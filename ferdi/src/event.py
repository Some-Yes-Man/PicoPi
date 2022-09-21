
from ferdi.src.EVENT_MAPPING import EVENT_MAPPING

"""
    Idea is to map incomming Events,
"""

class event:

    def __init__(self, pin):
        self.pin = pin
        self.myCallable = EVENT_MAPPING[self.pin]

    def __call__(self):
        self.myCallable()

    def setMyCallable(self, newFunction):
        self.myCallable = newFunction

    def handlePin_1(self):
        return True

    def handlePin_2(self):
        return True







