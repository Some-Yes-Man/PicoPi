import utime
from time import sleep_ms

dit = 500
read_intervall = int(dit/10)

dah = 3*dit
between_symbol = 1*dit
between_letters = 3*dit
between_words = 7*dit

MorseCodes = {
    'a': 'sl',
    'b': 'lsss',
    'c': 'lsls',
    'd': 'lss',
    'e': 's',
    'f': 'ssls',
    'g': 'lls',
    'h': 'ssss',
    'i': 'ss',
    'j': 'slll',
    'k': 'lsl',
    'l': 'slss',
    'm': 'll',
    'n': 'ls',
    'o': 'lll',
    'p': 'slls',
    'q': 'llsl',
    'r': 'sls',
    's': 'sss',
    't': 'l',
    'u': 'ssl',
    'v': 'sssl',
    'w': 'sll',
    'x': 'lssl',
    'y': 'lsll',
    'z': 'llss',
    '1': 'sllll',
    '2': 'sslll',
    '3': 'sssll',
    '4': 'ssssl',
    '5': 'sssss',
    '6': 'lssss',
    '7': 'llsss',
    '8': 'lllss',
    '9': 'lllls',
    '0': 'lllll'
}

MorseCodes_rev = {
    'sl': 'a',
    'lsss': 'b',
    'lsls': 'c',
    'lss': 'd',
    's': 'e',
    'ssls': 'f',
    'lls': 'g',
    'ssss': 'h',
    'ss': 'i',
    'slll': 'j',
    'lsl': 'k',
    'slss': 'l',
    'll': 'm',
    'ls': 'n',
    'lll': 'o',
    'slls': 'p',
    'llsl': 'q',
    'sls': 'r',
    'sss': 's',
    'l': 't',
    'ssl': 'u',
    'sssl': 'v',
    'sll': 'w',
    'lssl': 'x',
    'lsll': 'y',
    'llss': 'z',
    'sllll': '0',
    'sslll': '1',
    'sssll': '2',
    'ssssl': '3',
    'sssss': '4',
    'lssss': '5',
    'llsss': '6',
    'lllss': '7',
    'lllls': '8',
    'lllll': '9'
}

def send_sync(led):
    for i in range(5):
        led.led_for(dit)
        sleep_ms(between_symbol)

def analyse_dit_length(ldr):
    count_sync = 0
    length_list = []
    while count_sync < 5:
        start_time = utime.ticks_ms()
        while ldr.value():
            sleep_ms(1)
        while ldr.value() == 0:
            sleep_ms(1)
        end_time = utime.ticks_ms()
        length_list.append(end_time - start_time)
        count_sync = count_sync + 1
    length = 0
    for i in range (5):
        length += length_list[i]
    length /= 5
    return length

def set_dit_length(val):
    global dit, read_intervall, dah, between_letters, between_symbol, between_words
    dit = val
    read_intervall = int(dit/10)
    dah = 3*dit
    between_symbol = 1*dit
    between_letters = 3*dit
    between_words = 7*dit

def send(text, led):
    for c in text:
        if c == ' ':
            sleep_ms(between_words-between_letters)
        else:
            if c.lower() in MorseCodes:
                letter(MorseCodes[c.lower()], led)
    return

def letter(code, led):
    for c in code:
        if c == 's':
            led.led_for(dit)
        else:
            led.led_for(dah)
        sleep_ms(between_symbol)
    sleep_ms(between_letters-between_symbol)
    
def count_following(data, start):
    count = 0
    for i in range(start, len(data)):
        if data[i] == data[start]:
            count = count + 1
        else:
            break
    return count

def translate_to_morse(data):
    res = ""
    index = 0
    while (index < len(data)):
        count = count_following(data, index)
        if data[index] == 1:
            if count > between_letters/read_intervall:
                res = res + " - "
            elif count > between_symbol/read_intervall:
                res = res + " "
        else:
            if count > dit/read_intervall:
                res = res + "l"
            else:
                res = res + "s"
        index = index + count
    return res
    
def translate_to_text(data):
    data = translate_to_morse(data)
    res = ""
    for x in data.split():
        if x == "-":
            res = res + " "
        elif x in MorseCodes_rev:
            res = res + MorseCodes_rev[x]
        else:
            res = res + "-"
    return res