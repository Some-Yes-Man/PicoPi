import random
import math
from christmas.canvas import Canvas
from christmas.patternqueue import PatternQueue

from christmas.patterns.star import StarPattern

class TwinkleQueue(PatternQueue):
  def __init__(self, canvas: Canvas = None, stars: int = 10,
               red: int = 100, green: int = 100, blue: int = 100,
               deviationRed: int = 0, deviationGreen: int = 0, deviationBlue: int = 0,
               deviationRedPos: int = 0, deviationGreenPos: int = 0, deviationBluePos: int = 0,
               deviationRedNeg: int = 0, deviationGreenNeg: int = 0, deviationBlueNeg: int = 0,
               ):
    super().__init__(canvas=canvas, description="Twinkle Twinkle")
    for i in range(stars):
      r = max(0, min(255, red + deviationRed + deviationRedPos))
      minR = max(0, min(255, red - deviationRed - deviationRedNeg))
      g = max(0, min(255, green + deviationGreen + deviationGreenPos))
      minG = max(0, min(255, green - deviationGreen - deviationGreenNeg))
      b = max(0, min(255, blue + deviationBlue + deviationBluePos))
      minB = max(0, min(255, blue - deviationBlue - deviationBlueNeg))
      if (r != minR):
        r = random.randint(minR, r)
      if (g != minG):
        g = random.randint(minG, g)
      if (b != minB):
        b = random.randint(minB, b)

      self.addPattern(StarPattern(red=r, green=g, blue=b))

if __name__ == "__main__":
  from xmas import canvas
  s = TwinkleQueue(canvas=canvas, stars=25, red=30, green=50, blue=50, deviationRedPos=200)
  canvas.clear()
  while True:
    #canvas.clear()
    s.run()
    canvas.show()