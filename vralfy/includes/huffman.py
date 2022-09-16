from includes.morse import Morse
# https://en.wikipedia.org/wiki/Letter_frequency
probabilities = {
  'en': {
    'a': 0.082,
    'b': 0.015,
    'c': 0.028,
    'd': 0.043,
    'e': 0.13,
    'f': 0.022,
    'g': 0.02,
    'h': 0.061,
    'i': 0.07,
    'j': 0.0015,
    'k': 0.0077,
    'l': 0.04,
    'm': 0.024,
    'n': 0.067,
    'o': 0.075,
    'p': 0.019,
    'q': 0.00095,
    'r': 0.06,
    's': 0.063,
    't': 0.091,
    'u': 0.028,
    'v': 0.0098,
    'w': 0.024,
    'x': 0.0015,
    'y': 0.02,
    'z': 0.00074,
  },
  'en_dict': {
    'a': 0.078,
    'b': 0.02,
    'c': 0.04,
    'd': 0.038,
    'e': 0.11,
    'f': 0.014,
    'g': 0.03,
    'h': 0.023,
    'i': 0.086,
    'j': 0.0021,
    'k': 0.0097,
    'l': 0.053,
    'm': 0.027,
    'n': 0.072,
    'o': 0.061,
    'p': 0.028,
    'q': 0.0019,
    'r': 0.073,
    's': 0.087,
    't': 0.067,
    'u': 0.033,
    'v': 0.01,
    'w': 0.0091,
    'x': 0.0027,
    'y': 0.016,
    'z': 0.0044,
  },
  'de': {
    'a': 0.0651,
    'b': 0.0189,
    'c': 0.0306,
    'd': 0.0508,
    'e': 0.1740,
    'f': 0.0166,
    'g': 0.0301,
    'h': 0.0476,
    'i': 0.0755,
    'j': 0.0027,
    'k': 0.0121,
    'l': 0.0344,
    'm': 0.0253,
    'n': 0.0978,
    'o': 0.0251,
    'p': 0.0079,
    'q': 0.0002,
    'r': 0.0700,
    's': 0.0727,
    't': 0.0615,
    'u': 0.0435,
    'v': 0.0067,
    'w': 0.0189,
    'x': 0.0003,
    'y': 0.0004,
    'z': 0.0113,
    'ß': 0.0031,
  },
}

class HuffmanNode():
  def __init__(self, probability, symbol, left = None, right = None):
    self.probability = probability
    self.symbol = symbol
    self.left = left
    self.right = right
    self.code = ''

class Huffman(Morse):
  def __init__(self, dict = 'en'):
    nodes = []
    self.alphabet = {' ': ' '}
    self.dit = '.'
    self.dah = '-'
    self.binary_high = '1'
    self.binary_low = '0'
    self.pause = ''

    for symbol in probabilities[dict].keys():
      nodes.append(HuffmanNode(probabilities[dict][symbol], symbol))
    while len(nodes) > 1:
      nodes = sorted(nodes, key = lambda x: x.probability)
      left = nodes[0]
      right = nodes[1]
      # print('merging ' + left.symbol + ' and ' + right.symbol)
      newNode = HuffmanNode(left.probability + right.probability, left.symbol + right.symbol, left = left, right = right)
      nodes.remove(left)
      nodes.remove(right)
      nodes.append(newNode)
    root = nodes[0]
    self.calcCode(root)

  def calcCode(self, node, prefix = '', leftCode = None, rightCode = None):
    if leftCode == None: leftCode = self.dit
    if rightCode == None: rightCode = self.dah

    code = prefix + node.code
    if (node.left): self.calcCode(node.left, code + leftCode)
    if (node.right): self.calcCode(node.right, code + rightCode)
    if (not node.left and not node.right):
      node.code = code
      self.alphabet[node.symbol] = node.code
      print(node.symbol + ': ' + node.code + ' ' + self.alphabet[node.symbol])

  def morseToBinary(self, morse, dit = None, dah = None, pause=None, high = None, low = None):
    if dit == None: dit = self.dit
    if dah == None: dah = self.dah
    if pause == None: pause = self.pause
    if high == None: high = self.binary_high
    if low == None: low = self.binary_low

    ret = ""
    for c in morse:
      if c == dit: ret += high
      elif c == dah: ret += low
      elif c == pause: ret += ''
    return ret

  def binaryToMorse(self, binary, dit = None, dah = None, pause=None, high = None, low = None):
    if dit == None: dit = self.dit
    if dah == None: dah = self.dah
    if pause == None: pause = self.pause
    if high == None: high = self.binary_high
    if low == None: low = self.binary_low

    ret = ''
    for c in binary:
      if (c == high): ret += dit
      elif (c == low): ret += dah
    return ret
