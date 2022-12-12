from christmas.canvas import Canvas
from christmas.pattern import Pattern

class SnakePattern(Pattern):
  def __init__(self, canvas: Canvas=None, length=2, red=0, green=0, blue=0, fade=0):
    super().__init__(canvas=canvas, description="A snake pattern")
    self.length = length
    self.red = red
    self.green = green
    self.blue = blue
    self.fade = fade

  def render(self):
    for i in range(self.length):
      self.canvas.rgb((self.step + i) % self.canvas.get_ws().count(), 0, 0, 0)

    self.step = (self.step + 1) % self.canvas.get_ws().count()

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

if __name__ == "__main__":
  from xmas import canvas
  s = SnakePattern(canvas=canvas, length=5, red=150)
  while True:
    canvas.clear()
    s.run()
    canvas.show()