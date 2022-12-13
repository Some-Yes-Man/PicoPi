from christmas.canvas import Canvas
from christmas.pattern import Pattern

class FillPattern(Pattern):
  def __init__(self, canvas: Canvas= None, red: int = 0, green: int = 0, blue: int = 0):
    super().__init__(canvas=canvas, description="Fills canvas with one color")
    self.red = red
    self.green = green
    self.blue = blue

  def render(self):
    self.canvas.clear(r=self.red, g=self.green, b=self.blue)

if __name__ == "__main__":
  from xmas import canvas
  s = FillPattern(canvas=canvas, red=255, green=20, blue=20)
  s.run()
  canvas.show()