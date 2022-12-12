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
  def __init__(self, canvas: Canvas = None, duration: int = 2000):
    super().__init__(canvas=canvas, description="A Slideshow")
    self.duration = duration
    self.step = 0
    self.patternPos = 0

    self.addPattern(ClearPattern())
    self.addPattern(FillPattern(red=150))
    self.addPattern(ModPattern())
    self.addPattern(SnakePattern(blue=150))
    self.addPattern(StarPattern(green=150))

    self.addPattern(SnakeQueue())
    self.addPattern(TwinkleQueue(stars=60, red=30, green=50, blue=50, deviationRedPos=200))

  def run(self):
    self.queue[self.patternPos].run()
    if (self.patternPos == 0):
      self.patternPos = self.patternPos + 1
    else:
      self.step = (self.step + 1) % self.duration
      if (self.step == 0):
        self.patternPos = (self.patternPos + 1) % len(self.queue)
        print(self.patternPos, self.queue[self.patternPos].getDescription())

if __name__ == "__main__":
  from xmas import canvas
  s = SlideshowQueue(canvas=canvas)
  canvas.clear()
  while True:
    #canvas.clear()
    s.run()
    canvas.show()