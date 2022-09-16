import utime
from time import sleep_ms
from machine import *
from led import Led
import morse
from weather import Weather
import lcd

ldr = Pin(28, Pin.IN)
touch = machine.Pin(22, Pin.IN)
button = Pin(12, Pin.IN)

led_on_board = Led(25)
white_led = Led(13)
w = Weather()

mode = 1
max_mode = 4

last_tmp = 0
last_pres = 0

def btn_debounce(pin):
    Timer().init(mode=Timer.ONE_SHOT, period=200, callback=nextMode)

def nextMode(timer):
    global mode
    global last_pres
    print("press ", str(mode))
    last_pres = 0
    mode = mode + 1
    if mode > max_mode:
        mode = mode % max_mode

button.irq(trigger=Pin.IRQ_RISING, handler=btn_debounce)

morse_data = []
count_zero = 0
morse_started = False
morse_text = ""

while True:
    if mode == 1: # read in morse code
        if count_zero > morse.between_words/morse.read_intervall:
            print("fin")
            morse_text = morse.translate_to_text(morse_data)
            lcd.show(morse_text)
            count_zero = 0
            morse_started = False
            morse_text = ""
            morse_data = []
        elif morse_started == True:
            print("start")
            morse_data.append(ldr.value())
            if ldr.value()==0:
                count_zero = 0
            else:
                count_zero = count_zero + 1
        elif ldr.value() == 0:
            morse_started = True
            morse_data.append(ldr.value())
        sleep_ms(morse.read_intervall)
    elif mode == 2: # morse fixed text
        text = "e"
        lcd.show(text)
        morse.send(text, white_led)
    elif mode == 3: # morse with touch
        if touch.value() == 1:
            led_on_board.led_on()
        else:
            led_on_board.led_off()
        sleep_ms(50)
    else: # show temperature data
        if last_pres == 0:
            lcd.show("Temp: "+ str(w.getTemperature())+ "°C\np: "+ str(w.getPressure())+"Pa")
        if last_pres != w.getPressure():
            lcd.show_at(str(w.getPressure()), 3, 1)
            last_pres = w.getPressure()
        if last_tmp != w.getTemperature():
            lcd.show_at(str(w.getTemperature()), 6, 0)
            last_tmp = w.getTemperature()
        sleep_ms(100)
            
            
