from christmas.canvas import Canvas
from christmas.pattern import Pattern

class PatternQueue(Pattern):
  queue = []

  def __init__(self, canvas: Canvas, description: str = "A pattern queue", **kwargs):
    super().__init__(canvas=canvas, description=description, **kwargs)
    self.queue = []
    self.setCanvas(canvas)

  def setParameters(self, **kwargs):
    super().setParameters(**kwargs)
    for pattern in self.queue:
      pattern.setParameters(**kwargs)

  def addPattern(self, pattern: Pattern):
    pattern.setCanvas(self.canvas)
    pattern.setParameters(**self.kwargs)
    self.queue += [pattern]

  def setCanvas(self, canvas: Canvas):
    self.canvas = canvas
    for pattern in self.queue:
      pattern.setCanvas(self.canvas)

  def render(self):
    for pattern in self.queue:
      pattern.run()

if __name__ == "__main__":
  print("This is not a program")