from christmas.canvas import Canvas

numberOfLED = 128
canvas=Canvas(numberOfLED=numberOfLED)
canvas.set_rows(8)

if __name__ == "__main__":
  import includes.constants as const
  from christmas.queues.snake import SnakeQueue
  from time import sleep

  const.ONBOARD_LED.value(1)
  renderer=[
    SnakeQueue(canvas=canvas),
  ]
  current_renderer=0
  const.ONBOARD_LED.value(0)
  while True:
    #sleep(0.02)
    canvas.clear()
    renderer[current_renderer].run()
    canvas.show()
