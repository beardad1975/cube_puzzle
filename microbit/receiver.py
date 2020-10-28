import radio
from microbit import *
import ustruct

uart.init(115200)

radio.on()
#radio.config(channel = 9,group = 48,data_rate=radio.RATE_2MBIT)
radio.config(channel = 9,group = 48)

while True:
    display.clear()
    data = radio.receive_bytes()
    if data and len(data) == 10 :
        display.set_pixel(2,2,3)
        uart.write(data)
        #t = ustruct.unpack('!BBhhhBB', data)
        #print(t)
    sleep(50)
