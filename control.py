import serial
import struct
import time
from ursina import lerp

import common

class InputResult:
    def __init__(self, x, y, z, a, b):
        self.x = x
        self.y = y
        self.z = z
        self.a = True if a == 1 else False
        self.b = True if b == 1 else False


def serial_init():
    common.ser = serial.Serial(common.port, 115200, timeout=0)


def serial_flush():
    common.ser.reset_input_buffer()


def read_microbit():
    data = common.ser.read(10)
    if data and len(data) == 10:
        t = struct.unpack('!BBhhhBB', data)
        if t[0] == 255 and  t[1] == 0:
            return InputResult(t[2], t[3], t[4], t[5], t[6])
    return None
    

def map_value(x, in_min, in_max, out_min, out_max):
    return ((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)


def control_camera_return_ab():
    result = read_microbit()
    if result:

        x_degree = map_value(result.x, -1024, 1024, -120,120)
        y_degree = map_value(result.y, -1024, 1024, 120,-120)
        
        #if common.last_x:
        x_degree = lerp(common.last_x, x_degree, 0.3)
        #if common.last_y:
        y_degree = lerp(common.last_y, y_degree, 0.3)
                    
        common.puzzle_camera.rotation_y = x_degree
        common.puzzle_camera.rotation_x = y_degree

        common.last_x = x_degree
        common.last_y = y_degree

        return(result.a, result.b)
    return None, None


def control_cube_return_ab():
    result = read_microbit()
    if result:
        print('{:5} {:5} {:5} {:5} {:5}'.format(result.x, result.y, result.z, result.a, result.b))

        x_degree = map_value(result.x, -500, 500, -50,50)
        #y_degree = map_value(result.y, -800, 800, -50,50)
        z_degree = map_value(result.z, -500, 500, -50,50)
        
        #if common.last_x:
        x_degree = lerp(common.last_x, x_degree, 0.3)
        #if common.last_y:
        z_degree = lerp(common.last_z, z_degree, 0.3)
                    
        common.puzzle_camera.rotation_y = x_degree
        common.puzzle_camera.rotation_x = z_degree

        common.last_x = x_degree
        common.last_z = z_degree
        
        if common.level == common.HARD_LEVEL:
            common.state_machine.calc_target_and_update3x3()
        else:
            common.state_machine.calc_target_and_update2x2()
        return(result.a, result.b)
    return None, None



def return_ab():
    result = read_microbit()
    
    if result:
        print('{:5} {:5} {:5} {:5} {:5}'.format(result.x, result.y, result.z, result.a, result.b))
        return(result.a, result.b)
    return None, None
