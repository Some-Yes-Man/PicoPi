import network
import rp2
import socket
import time
import ubinascii
import _thread

from config.wlan import config as cfg

class WLAN:
  wlan: network.WLAN = None

  def __init__(self):
    rp2.country(cfg['COUNTRY'])
    self.wlan = network.WLAN(network.STA_IF)
    self.wlan.active(True)
    self.mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()

  def connect(self):
    retry = cfg['RETRY']
    print('Connecting WLAN', )
    while retry != 0:
      timeout = cfg['TIMEOUT']
      self.wlan.connect(cfg['SSID'], cfg['PASSWORD'])
      while timeout > 0:
        if self.wlan.status() < 0 or self.wlan.status() > 2:
          timeout = 0
        else:
          timeout -= 1
          print(timeout, '..')
          time.sleep(1)
      if self.wlan.status() != 3:
        retry = max(-1, retry - 1)
        print('Connection attempts left:', retry)
      else:
        retry = 0

    self.debug()
    if self.wlan.status() != 3:
      raise RuntimeError('Wi-Fi connection failed')

  def createSocket(self, ip: str = '0.0.0.0', port: int = 80, buffersize: int = 1024, callback = None):
    t = _thread.start_new_thread(self.createSocketThread, (ip, port, buffersize, callback))
    print('Thread created')

  def createSocketThread(self, ip: str = '0.0.0.0', port: int = 80, buffersize: int = 1024, callback = None):
    addr = socket.getaddrinfo(ip, port)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Socket',ip,':',port,'created')
    while True:
      try:
        cl, addr = s.accept()
        request = str(cl.recv(buffersize))
        if callback == None:
          cl.send('HTTP/1.0 200 OK\r\n')
          cl.send('Content-type: text/html\r\n')
          cl.send('\r\n')
          cl.send('<html><body>')
          cl.send('<code>' + request + '</code>')
          cl.send('</body></html>')
        else:
          callback(self, addr, request, cl)
        cl.close()
      except OSError as e:
        cl.close()

  def status(self):
    status = self.wlan.status()
    if status == 0:
      return 'Link Down'
    if status == 1:
      return 'Link Join'
    if status == 2:
      return 'Link NoIp'
    if status == 3:
      return 'Link Up'
    if status == -1:
      return 'Link Fail'
    if status == -2:
      return 'Link NoNet'
    if status == -3:
      return 'Link BadAuth'

  def debug(self):
    print('MAC     : ', self.mac)
    print('SSID    : ', cfg['SSID'])
    print('PASSWORD: ', cfg['PASSWORD'])
    print('Country : ', cfg['COUNTRY'])
    print('Status  : ', self.wlan.status(), self.status())

    print('ifConfig: ')
    for i in self.wlan.ifconfig():
      print('-', i)

    if self.wlan.status() != 3:
      print('Scan    : ')
      for ap in self.wlan.scan():
        print('-', ap)

if __name__ == "__main__":
  def cb(wlan: WLAN, remoteaddr: socket._RetAddress, request: str, response: socket.socket):
    response.send('HTTP/1.0 200 OK\r\n')
    response.send('Content-type: text/html\r\n')
    response.send('\r\n')
    response.send('OK')
    print('Client connected from', remoteaddr)

  wlan = WLAN()
  wlan.connect()
  wlan.debug()
  wlan.createSocket(callback=cb)
#  wlan.createSocketThread(callback=cb)
  while True:
    print("Waiting for connections")
    time.sleep(10)