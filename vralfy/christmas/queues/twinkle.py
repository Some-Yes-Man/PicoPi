from christmas.canvas import Canvas
from christmas.patternqueue import PatternQueue

from christmas.patterns.star import StarPattern

class TwinkleQueue(PatternQueue):
  def __init__(self, canvas: Canvas = None, **kwargs):
    super().__init__(canvas=canvas, description="Twinkle Twinkle", **kwargs)
    stars = self.getParameter('stars', 10)
    for i in range(stars):
      self.addPattern(StarPattern(**self.kwargs))

  def setParameters(self, **kwargs):
    super().setParameters(**kwargs)
    stars = self.getParameter('stars', 10)
    if len(self.queue) != stars:
      self.queue = []
      for i in range(stars):
        self.addPattern(StarPattern(**self.kwargs))

if __name__ == "__main__":
  from xmas import canvas
  s = TwinkleQueue(canvas=canvas, stars=25, red=30, green=50, blue=50, deviationRedPos=200)
  canvas.clear()
  while True:
    #canvas.clear()
    s.run()
    canvas.show()