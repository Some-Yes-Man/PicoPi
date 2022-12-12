from christmas.canvas import Canvas

class Pattern:
  def __init__(self, canvas: Canvas = None, description: str = "A pattern"):
    self.setCanvas(canvas)
    self.step = 0
    self.description = description

  def getDescription(self):
    return self.description

  def setCanvas(self, canvas: Canvas):
    self.canvas = canvas

  def run(self):
    if (self.canvas == None):
      return
    self.render()

  def render(self):
    print("pls override")

if __name__ == "__main__":
  print("This is not a program")