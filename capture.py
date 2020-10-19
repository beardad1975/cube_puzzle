

import numpy as np
import cv2

import common 


import cube_puzzle



def init():
    # opencv
    common.cap = cv2.VideoCapture(0)
    common.cap.set(cv2.CAP_PROP_FRAME_WIDTH, common.PHOTO_WIDTH)
    common.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, common.PHOTO_HEIGHT)
    
def update_texture():
    retval, buf = common.cap.read()
    #print('buf', buf)
    buf = cv2.flip(buf, -1)
    buf = cv2.rectangle(buf, common.CAP_LEFT_TOP, common.CAP_RIGHT_BOTTOM,
                        (0,0,255),3)
    #print('photo_tex ', common.photo_tex)
    common.photo_tex.setRamImage(buf)
    common.photo_quad.setTexture(common.photo_tex)
    