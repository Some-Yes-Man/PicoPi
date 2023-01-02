class Clazz1:
  kwargs = {}
  def __init__(self, **kwargs):
    self.setArgs(**kwargs)

  def setArgs(self, **kwargs):
    for key,value in kwargs.items():
      self.kwargs[key] = value

  def pr(self):
    print(self.kwargs)

class Clazz2(Clazz1):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

if __name__ == "__main__":
  c = Clazz2(test=123, foo='bar')
  c.setArgs(bing=45)
  c.pr()