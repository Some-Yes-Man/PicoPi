from includes.oled import OLED
from includes.sensors import Sensors

oled = OLED()
sensors = Sensors()

while True:
    # Clear the oled display in case it has junk on it.
    oled.fill(0)
    # Blit the image from the framebuffer to the oled display
    oled.blit(OLED.buffer_raspberry, 96, 0)
    # Add some text
    oled.text("ADC0: "+str(round(sensors.getADC(0),2)),10,8)
    oled.text("ADC1: "+str(round(sensors.getADC(1),2)),10,20)
    oled.text("ADC2: "+str(round(sensors.getADC(2),2)),10,32)
    oled.show()
