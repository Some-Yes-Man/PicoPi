import includes.constants as const

class Sensors():
    def __init__(self):
        print("Sensors initiated")

    def getADC(self, adc=2):
        adc = const.getADC(adc)
        conversion_factor = 3.3 / (65535)
        return adc.read_u16() * conversion_factor

if __name__ == "__main__":
  print("This is not a program")