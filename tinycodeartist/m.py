import utime
from time import sleep_ms
from machine import *
from led import Led
import morse
from morse import *
from weather import Weather
from lcd import *
from debounced_input import *

def nextMode(pin, pressed, duration_ms):
    if (pressed):
        global mode, mode_changed
        print("press ", str(mode))
        mode = mode + 1
        mode_changed = True
        if mode > max_mode:
            mode = mode % max_mode

ldr = Pin(28, Pin.IN)
touch = Pin(22, Pin.IN)
button = DebouncedInput(12, nextMode, pin_pull=Pin.PULL_DOWN)

led_on_board = Led(25)
white_led = Led(13)
w = Weather()

mode = 1
max_mode = 4
mode_changed = True

last_tmp = 0
last_pres = 0

morse_data = []
count_zero = 0
morse_started = False
morse_text = ""

def read_morse(sensor_value):
    global morse_data, count_zero, morse_text, morse_started
    if count_zero > between_words/read_intervall:
        print("finished reading morse")
        morse_text = translate_to_text(morse_data)
        show(morse_text)
        count_zero = 0
        morse_started = False
        morse_data = []
    elif morse_started == True:
        morse_data.append(sensor_value)
        if sensor_value==0:
            count_zero = 0
        else:
            count_zero = count_zero + 1
    elif sensor_value == 0:
        set_dit_length(analyse_dit_length())
        print("started to read morse")
        morse_started = True
        morse_data.append(sensor_value)

def show_weather():
    global last_pres, last_tmp, mode_changed
    if mode_changed:
        show("Temp: "+ str(w.getTemperature())+ chr(176)+"C\n")
        show_at("p: "+ str(w.getPressure())+"Pa", 0, 1)
        mode_changed = False
    if last_pres != w.getPressure():
        show_at(str(w.getPressure()), 3, 1)
        last_pres = w.getPressure()
    if last_tmp != w.getTemperature():
        show_at(str(w.getTemperature()), 6, 0)
        last_tmp = w.getTemperature()

while True:
    if mode == 1:
        if mode_changed:
            show("waiting for morse (light)")
            mode_changed = False
        else:
            read_morse(ldr.value())
            morse_text = ""
            sleep_ms(read_intervall)
    elif mode == 2:
        if mode_changed:
            set_dit_length(50)
            mode_changed = False
            text = "Hallo Welt, kannst du mich hören?"
            show_in_loop("morsing: "+text)
            send_sync(white_led)
        send(text, white_led)
    elif mode == 3:
        if mode_changed:
            set_dit_length(500)
            show("waiting for morse (touch)")
            mode_changed = False
        read_morse(not touch.value())
        if morse_text != "":
            set_dit_length(50)
            send_sync(white_led)
            send(morse_text, white_led)
            morse_text = ""
            set_dit_length(500)
        sleep_ms(read_intervall)
    else:
        show_weather()
        sleep_ms(100)
