import includes.constants as const
from christmas.canvas import Canvas
from christmas.snake import SnakeRenderer
from time import sleep

const.ONBOARD_LED.value(1)
numberOfLED = 128

canvas=Canvas(numberOfLED=numberOfLED)
canvas.set_rows(8)

renderer=[
  SnakeRenderer(canvas=canvas,length=10,green=255,fade=10),
]
current_renderer=0

const.ONBOARD_LED.value(0)
while True:
  #sleep(0.02)
  renderer[current_renderer].run()
  canvas.show()
