import math
import random
from christmas.canvas import Canvas
from christmas.pattern import Pattern

class StarPattern(Pattern):
  def __init__(self, canvas: Canvas=None, **kwargs):
    super().__init__(canvas=canvas, description="A star pattern", **kwargs)

  def randomize(self):
    minFade = self.getParameter('minFade', 100)
    maxFade = self.getParameter('maxFade', 300)
    minDuration = self.getParameter('minDuration', 50)
    maxDuration = self.getParameter('maxDuration', 150)

    self.animate = random.randint(0,1000) < 200
    self.position = random.randint(0, self.canvas.get_ws().count()-1)
    self.step = 0
    self.fade = random.randint(minFade, maxFade)
    self.duration = random.randint(minDuration, maxDuration)

    self.red = self.getParameter('red', 255)
    self.green = self.getParameter('green', 255)
    self.blue = self.getParameter('blue', 255)
    deviationRed = self.getParameter('deviationRed', 0)
    deviationGreen = self.getParameter('deviationGreen', 0)
    deviationBlue = self.getParameter('deviationBlue', 0)
    deviationRedPos = self.getParameter('deviationRedPos', 0)
    deviationGreenPos = self.getParameter('deviationGreenPos', 0)
    deviationBluePos = self.getParameter('deviationBluePos', 0)
    deviationRedNeg = self.getParameter('deviationRedNeg', 0)
    deviationGreenNeg = self.getParameter('deviationGreenNeg', 0)
    deviationBlueNeg = self.getParameter('deviationBlueNeg', 0)

    r = max(0, min(255, self.red + deviationRed + deviationRedPos))
    minR = max(0, min(255, self.red - deviationRed - deviationRedNeg))
    g = max(0, min(255, self.green + deviationGreen + deviationGreenPos))
    minG = max(0, min(255, self.green - deviationGreen - deviationGreenNeg))
    b = max(0, min(255, self.blue + deviationBlue + deviationBluePos))
    minB = max(0, min(255, self.blue - deviationBlue - deviationBlueNeg))
    if (r != minR):
      self.red = random.randint(minR, r)
    if (g != minG):
      self.green = random.randint(minG, g)
    if (b != minB):
      self.blue = random.randint(minB, b)

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