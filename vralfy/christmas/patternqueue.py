from christmas.canvas import Canvas
from christmas.pattern import Pattern

class PatternQueue(Pattern):
  queue = []

  def __init__(self, canvas: Canvas, description: str = "A pattern queue"):
    super().__init__(canvas=canvas, description=description)
    self.queue = []
    self.setCanvas(canvas)

  def addPattern(self, pattern: Pattern):
    pattern.setCanvas(self.canvas)
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