
from ursina import *
import numpy as np
import cv2
from panda3d.core import Texture

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

def pngOverlay(img, pngImg):
    alpha = pngImg[:,:,3] / 255.0
    alpha_3 = cv2.merge([alpha, alpha, alpha])
    
    png_bgr = pngImg[:,:,:3]
    result_img = (png_bgr*alpha_3 + img*(1-alpha_3)) 
    
    # NB: change type to uint8
    print(np.sum(result_img >200))

    return result_img.astype(np.uint8)

def make_cube_texture():
    # clean old texture and cube
    retval, buf = common.cap.read()
    common.buf = cv2.flip(buf, -1)
    
    for i in common.cube_tex_list:
        del i
    for i in common.cube_list:
        del i
    common.cube_tex_list = []
    common.cube_list = []
    
    # 3x3    
    if common.level == common.MEDIUM_LEVEL:
        print('---here---')
        # make new cube
        border3x3 = cv2.imread('border3x3.png', cv2.IMREAD_UNCHANGED)
        
        for i in range(-1,2):
            for j in range(-1,2):
                e = Entity(model='cube', x=j, y=i,)
                common.cube_list.append(e)

        # make new texture
        for i in range(3):
            for j in range(3):
                tex = Texture()
                size = common.TEX_SIZE_3X3
                tex.setup2dTexture(size, size,
                                   Texture.T_unsigned_byte, Texture.F_rgb8)
                start_x, start_y = common.CAP_LEFT_TOP
                buf1 = common.buf[start_y+size*i:start_y+size*(i+1),
                                  start_x+size*j:start_x+size*(j+1)].copy()
                buf1 = pngOverlay(buf1, border3x3)
                tex.setRamImage(buf1)
                common.cube_tex_list.append(tex)

        # apply textures to cubes
        for i in range(9):
            common.cube_list[i].setTexture(common.cube_tex_list[i])
            
            
            

    