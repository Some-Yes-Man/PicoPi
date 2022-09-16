from machine import Pin
import time
from time import sleep_ms

class Led:
    def __init__(self, pin):
        self.led = Pin(pin, Pin.OUT)
        self.pin = pin

    def led_for(self, time):
        self.led_on()
        sleep_ms(time)
        self.led_off()

    def led_on(self):
        self.led.value(1)
        
    def led_off(self):
        self.led.value(0)
