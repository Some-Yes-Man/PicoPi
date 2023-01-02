from christmas.canvas import Canvas
from christmas.pattern import Pattern

class SnakePattern(Pattern):
  def __init__(self, canvas: Canvas=None, **kwargs):
    super().__init__(canvas=canvas, description="A snake pattern", **kwargs)

  def render(self):
    length = self.getParameter('length', 2)
    red = self.getParameter('red', 0)
    green = self.getParameter('green', 0)
    blue = self.getParameter('blue', 0)
    fade = self.getParameter('fade', 0)

    for i in range(length):
      self.canvas.rgb((self.step + i) % self.canvas.get_ws().count(), 0, 0, 0)

    self.step = (self.step + 1) % self.canvas.get_ws().count()

    for i in range(length):
      self.canvas.rgb((self.step + i) % self.canvas.get_ws().count(), red, green, blue)

    col = length // 2
    for i in range(col):
      r = red
      g = green
      b = blue
      if (fade > 0):
        r = (red) * (i+1) // (fade * (col+1))
        g = (green) * (i+1) // (fade * (col+1))
        b = (blue) * (i+1) // (fade * (col+1))
      #print(r,g,b)
      self.canvas.rgb((self.step + i) % self.canvas.get_ws().count(), r, g, b)
      self.canvas.rgb((self.step + length - i) % self.canvas.get_ws().count(), r, g, b)

if __name__ == "__main__":
  from xmas import canvas
  s = SnakePattern(canvas=canvas, length=5, red=150)
  while True:
    canvas.clear()
    s.run()
    canvas.show()