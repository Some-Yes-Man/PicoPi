from christmas.canvas import Canvas

class Pattern:
  kwargs = {}
  def __init__(self, canvas: Canvas = None, description: str = "A pattern", **kwargs):
    self.setCanvas(canvas)
    self.step = 0
    self.description = description
    self.setParameters(**kwargs)

  def getDescription(self):
    return self.description

  def getParameter(self, name: str, defaultValue):
    if name not in self.kwargs:
      self.kwargs[name] = defaultValue
      #print(self.description, self.kwargs)
    if type(defaultValue) is int:
      return int(self.kwargs[name])
    elif type(defaultValue) is str:
      return str(self.kwargs[name])
    else:
      return self.kwargs[name]

  def setParameters(self, **kwargs):
    for key,value in kwargs.items():
      self.kwargs[key] = value
    #print(self.description, self.kwargs)

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