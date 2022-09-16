from machine import *
from bmp280 import *
from time import sleep_ms

class Weather:
    def __init__(self):
        i2c2 = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
        bmp280_object = BMP280(i2c2, addr = 118, use_case = BMP280_CASE_WEATHER)
        bmp280_object.power_mode = BMP280_POWER_NORMAL
        bmp280_object.oversample = BMP280_OS_HIGH
        bmp280_object.temp_os = BMP280_TEMP_OS_8
        bmp280_object.press_os = BMP280_TEMP_OS_4
        bmp280_object.standby = BMP280_STANDBY_250
        bmp280_object.iir = BMP280_IIR_FILTER_2
        self.bmp = bmp280_object
        
    def getTemperature(self):
        return self.bmp.temperature

    def getPressure(self):
        return self.bmp.pressure
