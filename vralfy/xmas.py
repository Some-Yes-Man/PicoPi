from christmas.canvas import Canvas

numberOfLED = 128
canvas=Canvas(numberOfLED=numberOfLED)
canvas.set_rows(8)

if __name__ == "__main__":
  import includes.constants as const
  const.ONBOARD_LED.value(1)

  import includes.http as http
  from library.wlan import WLAN
  import json
  import socket
  import time
  import _thread

  from christmas.queues.slideshow import SlideshowQueue
  from christmas.queues.snake import SnakeQueue
  from christmas.queues.twinkle import TwinkleQueue
  from christmas.patterns.clear import ClearPattern
  from christmas.patterns.fill import FillPattern
  from christmas.patterns.mod import ModPattern
  from christmas.patterns.snake import SnakePattern
  from christmas.patterns.star import StarPattern

  renderer=[
    SlideshowQueue(canvas=canvas),
    SnakeQueue(canvas=canvas),
    TwinkleQueue(canvas=canvas),
    ClearPattern(canvas=canvas),
    FillPattern(canvas=canvas, red=255),
    ModPattern(canvas=canvas),
    SnakePattern(canvas=canvas, green=255),
    StarPattern(canvas=canvas),
  ]
  current_renderer=0

  def render_thread():
    while True:
      #time.sleep(0.02)
      canvas.clear()
      renderer[current_renderer].run()
      canvas.show()
  t = _thread.start_new_thread(render_thread, ())

  def cb(wlan: WLAN, remoteaddr: socket._RetAddress, request: str, response: socket.socket):
    const.ONBOARD_LED.toggle()
    r = http.parse(request)

    response.send('HTTP/1.0 200 OK\r\n')
    response.send('Content-type: text/json\r\n')
    response.send('\r\n')

    if 'led' in r['parameter']:
      v = r['parameter']['led']
      if v == 'on':
        const.ONBOARD_LED.value(1)
      elif v == 'off':
        const.ONBOARD_LED.value(0)
      elif v == 'toggle':
        const.ONBOARD_LED.toggle()
    elif 'list' in r['parameter']:
      r['renderer'] = {}
    elif 'renderer' in r['parameter']:
      v = int(r['parameter']['renderer'])
      global current_renderer
      current_renderer = min(len(renderer), max(0, v))

    r['leds'] = numberOfLED
    r['renderer'] = {}
    for idx in range(len(renderer)):
      r['renderer'][idx] = renderer[idx].getDescription()
    r['current_renderer'] = renderer[current_renderer].getDescription()
    response.send(json.dumps(r))
    const.ONBOARD_LED.toggle()

  const.ONBOARD_LED.value(0)
  wlan = WLAN()
  wlan.connect()
  wlan.createSocketThread(callback=cb)
