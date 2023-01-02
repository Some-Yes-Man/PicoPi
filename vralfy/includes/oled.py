import includes.constants as const
from library.ssd1306 import SSD1306_I2C

from machine import I2C
import framebuf

class OLED(SSD1306_I2C):
    array_raspberry = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    buffer_raspberry = framebuf.FrameBuffer(array_raspberry, 32, 32, framebuf.MONO_HLSB)

    def __init__(self, width=128, height=64, freq = 200000, i2cPosition = 2, i2cPorts = None):
        if i2cPorts == None: i2cPorts = const.getI2C0(i2cPosition)
        self.OLED_I2C = I2C(0, scl=i2cPorts[1], sda=i2cPorts[0], freq = freq)
        self.printDebug()
        super().__init__(width, height, self.OLED_I2C)
        print("OLED initiated")

    def printDebug(self):
        print("I2C Address      : "+hex(self.OLED_I2C.scan()[0]).upper())
        print("I2C Configuration: "+str(self.OLED_I2C))

if __name__ == "__main__":
  oled = OLED(i2cPosition=5)
  oled.fill(0)
  oled.text('hello there', 0, 40)
  oled.show()
