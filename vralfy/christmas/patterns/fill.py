from christmas.canvas import Canvas
from christmas.pattern import Pattern

class FillPattern(Pattern):
  def __init__(self, canvas: Canvas= None, **kwargs):
    super().__init__(canvas=canvas, description="Fills canvas with one color", **kwargs)

  def render(self):
    red = self.getParameter('red', 255)
    green = self.getParameter('green', 255)
    blue = self.getParameter('blue', 255)
    self.canvas.clear(r=red, g=green, b=blue)

if __name__ == "__main__":
  from xmas import canvas
  s = FillPattern(canvas=canvas, red=255, green=20, blue=20)
  s.run()
  canvas.show()