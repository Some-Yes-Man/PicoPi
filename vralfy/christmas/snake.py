from christmas.canvas import Canvas
from christmas.renderer import Renderer
class SnakeRenderer(Renderer):
  def __init__(self, canvas: Canvas, length=2, red=0, green=0, blue=0, fade=0):
    super().__init__(canvas=canvas)
    self.length = length
    self.red = red
    self.green = green
    self.blue = blue
    self.fade = fade

  def run(self):
    self.canvas.clear()
    for i in range(self.length):
      self.canvas.rgb((self.step + i) % self.canvas.get_ws().count(), self.red, self.green, self.blue)
    col = self.length // 2
    for i in range(col):
      r = self.red
      g = self.green
      b = self.blue
      if (self.fade > 0):
        r = (self.red) * (i+1) // (self.fade * (col+1))
        g = (self.green) * (i+1) // (self.fade * (col+1))
        b = (self.blue) * (i+1) // (self.fade * (col+1))
      #print(r,g,b)
      self.canvas.rgb((self.step + i) % self.canvas.get_ws().count(), r, g, b)
      self.canvas.rgb((self.step + self.length - i) % self.canvas.get_ws().count(), r, g, b)

    self.step = (self.step + 1) % self.canvas.get_ws().count()