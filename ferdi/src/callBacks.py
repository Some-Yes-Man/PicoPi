from ferdi.src.main import lS, pL_receive ,pL_send
from ferdi.src.EVENT_MAPPING import THE_EVENT_MAPPING, HAND_OVER_PARAMS
import uasyncio

async def cb1():
    print("#stub")
    # if THE_EVENT_MAPPING["id1"] == 0:
    #     THE_EVENT_MAPPING["id1"] = 1
    # else:
    #     THE_EVENT_MAPPING["id1"] = 0
    # return


class cb2:
    def __call__(self):
        cb2()

    async def cb2(self):
        print("#2 testing")
        if THE_EVENT_MAPPING["id2"] == 0:
            THE_EVENT_MAPPING["id2"] = 1
        else:
            THE_EVENT_MAPPING["id2"] = 0
        return


class morse_send_cb:
    def __call__(self):
        self.morse_send_()

    async def morse_send_(self):
        if THE_EVENT_MAPPING["id3"] == 0:
            THE_EVENT_MAPPING["id3"] = 1
        else:
            THE_EVENT_MAPPING["id3"] = 0
            print("morsing the given text now")
            toBeMorse = pL_receive.morseReceive(HAND_OVER_PARAMS["3"])
            await uasyncio.sleep_ms(500)
            pL_send.morseSend(toBeMorse)
            print("morsing of [" + str(toBeMorse) + "] happend.")
        return


class morse_receive_cb:
    def __call__(self):
        self.morse_receive_()

    async def morse_receive_(self):
        if THE_EVENT_MAPPING["id4"] == 0:
            THE_EVENT_MAPPING["id4"] = 1
        else:
            THE_EVENT_MAPPING["id4"] = 0
            print("receiving morse")
            result = pL_receive.morseReceive(HAND_OVER_PARAMS["5"])
            await uasyncio.sleep_ms(500)
            print("transforming morse into text")
            text = pL_receive.morseToText(result)
            print("the result is: " + str(text))
        return


class sync_morse_cb:
    def __call__(self):
        self.sync_morse_()

    async def sync_morse_(self):
        if THE_EVENT_MAPPING["id5"] == 0:
            THE_EVENT_MAPPING["id5"] = 1
        else:
            print("syncing for morsing started")
            THE_EVENT_MAPPING["id5"] = 0
            duration = lS.syncForMorse()
            HAND_OVER_PARAMS["5"] = duration
        return


CB_MAPPING = {"id1": cb1, "id2": cb1, "id3": morse_send_cb, "id4": morse_receive_cb, "id5": sync_morse_cb}

