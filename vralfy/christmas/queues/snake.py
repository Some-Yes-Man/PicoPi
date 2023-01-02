from christmas.canvas import Canvas
from christmas.patternqueue import PatternQueue

from christmas.patterns.snake import SnakePattern

class SnakeQueue(PatternQueue):
  def __init__(self, canvas: Canvas = None, **kwargs):
    super().__init__(canvas=canvas, description="Snake", **kwargs)
    self.addPattern(SnakePattern())

if __name__ == "__main__":
  from xmas import canvas
  s = SnakeQueue(canvas=canvas)
  while True:
    canvas.clear()
    s.run()
    canvas.show()