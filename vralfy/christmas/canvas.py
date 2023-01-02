from library.ws2801 import WS2801Pixels
import machine

class Canvas:
  def __init__(self,
               numberOfLED=1, rows=1, columns=1,
               clockPin=2, mosiPin=3, misoPin=4, bautrate=1000000,
               sleep=0):
    self._rows = rows
    self._columns = columns
    self._spi = machine.SPI(
      0,
      baudrate=bautrate,
      #polarity=1,
      #phase=1,
      bits=8,
      #firstbit=machine.SPI.MSB,
      sck=machine.Pin(clockPin),
      mosi=machine.Pin(mosiPin),
      miso=machine.Pin(misoPin)
      )
    self._ws = WS2801Pixels(numberOfLED, self._spi, sleep=sleep)

  def get_ws(self):
    return self._ws

  def set_rows(self, rows):
    self._rows = rows
    self._columns = self._ws.count() / self._rows
  def get_rows(self):
    return self._rows

  def set_columns(self, columns):
    self._columns = columns
    self._rows = self._ws.count() / self._columns
  def get_columns(self):
    return self._columns

  def clear(self,r=0,g=0,b=0):
    if (r==0 and g==0 and b==0):
      self._ws.clear()
    else:
      self._ws.set_pixels_rgb(r,g,b)
  def show(self):
    self._ws.show()
  def rgb(self, n=-1, r=0, g=0, b=0):
    self._ws.set_pixel_rgb(n,r,g,b)

  def draw(self, x, y, r=0, g=0, b=0):
    n = self._ws.count() // self._rows*y + x
    self._ws.set_pixel_rgb(n,r,g,b)

if __name__ == "__main__":
  print("This is not a program")