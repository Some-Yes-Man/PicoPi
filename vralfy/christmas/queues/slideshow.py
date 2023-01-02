from christmas.canvas import Canvas
from christmas.patternqueue import PatternQueue

from christmas.patterns.clear import ClearPattern
from christmas.patterns.fill import FillPattern
from christmas.patterns.mod import ModPattern
from christmas.patterns.snake import SnakePattern
from christmas.patterns.star import StarPattern

from christmas.queues.snake import SnakeQueue
from christmas.queues.twinkle import TwinkleQueue

class SlideshowQueue(PatternQueue):
  def __init__(self, canvas: Canvas = None, **kwargs):
    self.setParameters(**{
      'stars': 25,
      'red': 200,
      'green': 100,
      'blue': 100,
      'length': 10,
      'duration':250,
    })
    super().__init__(canvas=canvas, description="A Slideshow", **kwargs)
    self.step = 0
    self.patternPos = 0

    self.addPattern(ClearPattern())
    self.addPattern(FillPattern())
    self.addPattern(ModPattern())
    self.addPattern(SnakePattern())
    self.addPattern(StarPattern())

    self.addPattern(SnakeQueue())
    self.addPattern(TwinkleQueue())

  def setParameters(self, **kwargs):
    super().setParameters(**kwargs)

  def run(self):
    self.queue[self.patternPos].setParameters(**self.kwargs)
    self.queue[self.patternPos].run()
    if (self.patternPos == 0):
      self.patternPos = self.patternPos + 1
    else:
      self.step = (self.step + 1) % self.getParameter('duration', 1000)
      if (self.step == 0):
        self.patternPos = (self.patternPos + 1) % len(self.queue)
        print(self.patternPos, self.queue[self.patternPos].getDescription())

if __name__ == "__main__":
  from xmas import canvas
  s = SlideshowQueue(canvas=canvas, duration=10)
  canvas.clear()
  while True:
    #canvas.clear()
    s.run()
    canvas.show()