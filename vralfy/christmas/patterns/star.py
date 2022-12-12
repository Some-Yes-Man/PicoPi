import math
import random
from christmas.canvas import Canvas
from christmas.pattern import Pattern

class StarPattern(Pattern):
  def __init__(self, canvas: Canvas=None,
               red: int = 255, green: int = 255, blue: int = 255,
               minFade: int = 100, maxFade: int = 300,
               minDuration: int = 50, maxDuration: int = 150
               ):
    super().__init__(canvas=canvas, description="A star pattern")
    self.red = red
    self.green = green
    self.blue = blue
    self.minFade = minFade
    self.maxFade = maxFade
    self.minDuration = minDuration
    self.maxDuration = maxDuration
    #self.randomize()
    #self.step = random.randint(0, self.fade * 2 + self.duration)

  def randomize(self):
    self.animate = random.randint(0,1000) < 200
    self.position = random.randint(0, self.canvas.get_ws().count()-1)
    self.step = 0
    self.fade = random.randint(self.minFade, self.maxFade)
    self.duration = random.randint(self.minDuration, self.maxDuration)

  def render(self):
    if (self.step == 0):
      self.randomize()
    if (self.animate == False and self.step == 0):
      return

    r = self.red
    g = self.green
    b = self.blue
    if (self.step < self.fade):
      r = (r * self.step) // self.fade
      g = (g * self.step) // self.fade
      b = (b * self.step) // self.fade

    if (self.step > self.fade + self.duration):
      n = (self.fade * 2 + self.duration) - self.step
      r = (r * n) // self.fade
      g = (g * n) // self.fade
      b = (b * n) // self.fade

    self.canvas.rgb(self.position, r, g, b)
    self.step = (self.step + 1) % (self.fade * 2 + self.duration)
    if (self.step == 0):
      self.canvas.rgb(self.position, 0, 0, 0)

if __name__ == "__main__":
  from xmas import canvas
  star = StarPattern(canvas=canvas, red=180, green=100, blue=100)
  while True:
    canvas.clear()
    star.run()
    canvas.show()