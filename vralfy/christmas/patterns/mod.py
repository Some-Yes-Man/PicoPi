from christmas.canvas import Canvas
from christmas.pattern import Pattern

class ModPattern(Pattern):
  def __init__(self, canvas: Canvas= None, **kwargs):
    super().__init__(canvas=canvas, description="Alternating pattern ... good for counting", **kwargs)

  def render(self):
    for i in range(self.canvas.get_ws().count()):
      if (i % 50 == 0):
        self.canvas.rgb(i, 0,0,100)
      elif (i % 10 == 0):
        self.canvas.rgb(i, 0,100,0)
      elif (i % 5 == 0):
        self.canvas.rgb(i, 100,0,0)
      else:
        self.canvas.rgb(i, 0,0,0)

if __name__ == "__main__":
  from xmas import canvas
  canvas.clear()
  s = ModPattern(canvas=canvas)
  s.run()
  canvas.show()