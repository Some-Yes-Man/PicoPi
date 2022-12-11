from christmas.canvas import Canvas
class Renderer:
  def __init__(self, canvas: Canvas):
    self.canvas=canvas
    self.step = 0

  def run(self):
    print("override")