#from ferdi.src.main import setValueTo1
from ferdi.src.EVENT_MAPPING import THE_EVENT_MAPPING


async def cb1():
    print("#1")
        # if THE_EVENT_MAPPING["id1"] == 0:
        #     THE_EVENT_MAPPING["id1"] = 1
        # else:
        #     THE_EVENT_MAPPING["id1"] = 0
        # return

class cb2:
    def __call__(self):
        cb2()
    async def cb2(self):
        print("#2")
        if THE_EVENT_MAPPING["id2"] == 0:
            THE_EVENT_MAPPING["id2"] = 1
        else:
            THE_EVENT_MAPPING["id2"] = 0
        return

CB_MAPPING = {"id1":cb1, "id2":cb1}