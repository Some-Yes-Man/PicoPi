from christmas.canvas import Canvas
from christmas.pattern import Pattern

class ClearPattern(Pattern):
  def __init__(self, canvas: Canvas= None, **kwargs):
    super().__init__(canvas=canvas, description="Clears complete canvas", **kwargs)

  def render(self):
    self.canvas.clear()

if __name__ == "__main__":
  from xmas import canvas
  s = ClearPattern(canvas=canvas)
  s.run()
  canvas.show()