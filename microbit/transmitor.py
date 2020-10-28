import radio
from microbit import *
import ustruct

uart.init(115200)

radio.on()
radio.config(channel = 9,group = 48)

orix = 2
oriy = 2

while True:
    display.clear()
    
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    z = accelerometer.get_z()
    a = 1 if button_a.is_pressed() else 0
    b = 1 if button_b.is_pressed() else 0 
    
    posx = orix + x//400
    posx = max( min(posx, 4), 0)
    
    posy = oriy + y//400
    posy = max( min(posy, 4), 0)
    
    display.set_pixel(posx, posy, 3+a*2+b*2) 
    
    result = ustruct.pack('!BBhhhBB',255,0, x, y, z, a, b)
    uart.write(result)
    radio.send_bytes(result)
    sleep(100)
    

