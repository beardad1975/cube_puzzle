import random
import sys

from ursina import *
import numpy as np
import cv2
from panda3d.core import Texture

import common 
import cube_puzzle



def init():
    # opencv
    
    common.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    
    
    
    if not common.cap.isOpened():
        print('找不到攝影機，程式中斷')
        sys.exit()
    else:
        print('已啟動攝影機')
    
    common.cap.set(cv2.CAP_PROP_FRAME_WIDTH, common.PHOTO_WIDTH)
    common.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, common.PHOTO_HEIGHT)
    
def update_texture():
    retval, buf = common.cap.read()
    #print('buf', buf)
    buf = cv2.flip(buf, -1)
    if common.level == common.HARD_LEVEL:
        #print('here')
        x, y = common.CAP_LEFT_TOP
        size = common.TEX_SIZE_3X3
        # draw vertical lines
        for i in range(4):
            buf = cv2.line(buf, (x+size*i,y),(x+size*i,common.CAP_SQUARE_SIZE),
                           (0,255,255),15)
        # draw horizontal lines
        for i in range(1,3):
            buf = cv2.line(buf, (x,y+size*i),(x+common.CAP_SQUARE_SIZE,y+size*i),
                           (0,255,255),15)
    else:
        x, y = common.CAP_LEFT_TOP
        size = common.TEX_SIZE_2X2
        # draw vertical lines
        for i in range(3):
            buf = cv2.line(buf, (x+size*i,y),(x+size*i,common.CAP_SQUARE_SIZE),
                           (0,255,255),20)
        # draw horizontal lines
        for i in range(1,2):
            buf = cv2.line(buf, (x,y+size*i),(x+common.CAP_SQUARE_SIZE,y+size*i),
                           (0,255,255),20)
        
        
        
    #buf = cv2.rectangle(buf, common.CAP_LEFT_TOP, common.CAP_RIGHT_BOTTOM,
    #                    (0,0,255),3)
    
    #print('photo_tex ', common.photo_tex)
    common.photo_tex.setRamImage(buf)
    common.photo_quad.setTexture(common.photo_tex)

def pngOverlay(img, pngImg):
    alpha = pngImg[:,:,3] / 255.0
    alpha_3 = cv2.merge([alpha, alpha, alpha])
    
    png_bgr = pngImg[:,:,:3]
    result_img = (png_bgr*alpha_3 + img*(1-alpha_3)) 
    
    # NB: change type to uint8
    #print(np.sum(result_img >200))

    return result_img.astype(np.uint8)


def clean_cube_and_img():
    for i in common.cube_img_list:
        del i
        
    for i in common.cube_list:
        i.model = None
        del i
    for i in common.cube_border_list:
        del i
    common.cube_img_list = []
    common.cube_list = []
    common.cube_border_list = []

def make_cube_texture3x3():
    # clean old texture and cube
    retval, buf = common.cap.read()
    common.buf = cv2.flip(buf, -1)
    
    clean_cube_and_img()
    
    # 3x3    
    #if common.level == common.HARD_LEVEL:
    # load 6 kind of border and shuffle
    for i in range(6):
        border3x3 = cv2.imread(f'border3x3_{i}.png', cv2.IMREAD_UNCHANGED)
        common.cube_border_list.append(border3x3)
    random.shuffle(common.cube_border_list)
    
    # make new cube
    for i in (1, 0, -1):
        for j in (-1, 0, 1):
            e = Entity(model='cube_puzzle', x=j, y=i,)
            common.cube_list.append(e)

    start_x, start_y = common.CAP_LEFT_TOP
    size = common.TEX_SIZE_3X3
    # make 9 pieces of capture img
    for i in range(2,-1,-1):
        for j in range(3):
            
            buf_tmp = common.buf[start_y+size*i:start_y+size*(i+1),
                               start_x+size*j:start_x+size*(j+1)]
            
            common.cube_img_list.append(buf_tmp)
            
    # apply textures to cubes
    # 1st face: answer, 2~6th faces: random 
    for i in range(9):
        #common.cube_list[i].setTexture(common.cube_tex_list[i])
        tmp_img_list = []
        tmp_img_list.append(common.cube_img_list[i])
        tmp_img_list += random.sample(common.cube_img_list, 5)
        #assert len(tmp_img_list )== 6 , 'no 6 images'
        
        tmp_tex_buf = np.zeros((common.CAP_SQUARE_SIZE, common.CAP_SQUARE_SIZE,3),
                               dtype=np.uint8)
        # make six faces texture
        tmp_img_index = 0
        #tmp_tex_buf[480:720, 0:240] = (0,0,255)
        for j in (2, 1):
            for k in (0, 1, 2):
                buf_tmp = pngOverlay(tmp_img_list[tmp_img_index],
                                     common.cube_border_list[tmp_img_index]) 
                small_buf = tmp_tex_buf[common.TEX_SIZE_3X3*j : common.TEX_SIZE_3X3*(j+1),
                            common.TEX_SIZE_3X3*k : common.TEX_SIZE_3X3*(k+1)] \
                            =buf_tmp
               
                tmp_img_index += 1
        #print(tmp_tex_buf.shape)
        #import code;code.interact(local=dict(globals(), **locals()))
        #tmp_tex_buf = cv2.flip(tmp_tex_buf, -1)
        #if i == 0:
        #    ret = cv2.imwrite('tmp.jpg',tmp_tex_buf)
        
        tex = Texture()
        tex.setup2dTexture(common.TEX_SIZE_3X3 * 3, common.TEX_SIZE_3X3 * 3,
                           Texture.T_unsigned_byte, Texture.F_rgb8)
        tex.setRamImage(tmp_tex_buf)
        common.cube_list[i].setTexture(tex)
            
def make_cube_texture2x2():
    # clean old texture and cube
    retval, buf = common.cap.read()
    common.buf = cv2.flip(buf, -1)
    
    clean_cube_and_img()
    
    # 3x3    
    #if common.level == common.HARD_LEVEL:
    # load 6 kind of border and shuffle
    for i in range(6):
        border3x3 = cv2.imread(f'border3x3_{i}.png', cv2.IMREAD_UNCHANGED)
        common.cube_border_list.append(border3x3)
    random.shuffle(common.cube_border_list)
    
    # make new cube
    for i in (0.5, -0.5):
        for j in (-0.5, 0.5):
            e = Entity(model='cube_puzzle', x=j, y=i,)
            common.cube_list.append(e)

    start_x, start_y = common.CAP_LEFT_TOP
    size = common.TEX_SIZE_2X2
    # make 9 pieces of capture img
    for i in ( 1, 0):
        for j in (0, 1):
            
            buf_tmp = common.buf[start_y+size*i:start_y+size*(i+1),
                               start_x+size*j:start_x+size*(j+1)]
            #make small size to 3x3 texture
            buf_tmp = cv2.resize(buf_tmp, (common.TEX_SIZE_3X3, common.TEX_SIZE_3X3), interpolation = cv2.INTER_AREA)
            common.cube_img_list.append(buf_tmp)
            
    # apply textures to cubes
    # 1st face: answer, 2~6th faces: random 
    for i in range(4):
        #common.cube_list[i].setTexture(common.cube_tex_list[i])
        tmp_img_list = []
        tmp_img_list.append(common.cube_img_list[i])
        #tmp_img_list += random.sample(common.cube_img_list, 5)
        tmp_img_list += (random.sample(common.cube_img_list , 3) + random.sample(common.cube_img_list , 2))
        
        assert len(tmp_img_list )== 6 , 'no 6 images'
        
        tmp_tex_buf = np.zeros((common.CAP_SQUARE_SIZE, common.CAP_SQUARE_SIZE,3),
                               dtype=np.uint8)
        # make six faces texture
        tmp_img_index = 0
        #tmp_tex_buf[480:720, 0:240] = (0,0,255)
        for j in (2, 1):
            for k in (0, 1, 2):
                buf_tmp = pngOverlay(tmp_img_list[tmp_img_index],
                                     common.cube_border_list[tmp_img_index]) 
                small_buf = tmp_tex_buf[common.TEX_SIZE_3X3*j : common.TEX_SIZE_3X3*(j+1),
                            common.TEX_SIZE_3X3*k : common.TEX_SIZE_3X3*(k+1)] \
                            =buf_tmp
               
                tmp_img_index += 1
        #print(tmp_tex_buf.shape)
        #import code;code.interact(local=dict(globals(), **locals()))
        #tmp_tex_buf = cv2.flip(tmp_tex_buf, -1)
        #if i == 0:
        #    ret = cv2.imwrite('tmp.jpg',tmp_tex_buf)
        
        tex = Texture()
        tex.setup2dTexture(common.TEX_SIZE_3X3 * 3, common.TEX_SIZE_3X3 * 3,
                           Texture.T_unsigned_byte, Texture.F_rgb8)
        tex.setRamImage(tmp_tex_buf)
        common.cube_list[i].setTexture(tex)

def make_practice_cube2x2():
    # make new cube
    for i in (0.5, -0.5):
        for j in (-0.5, 0.5):
            e = Entity(model='cube_puzzle', x=j, y=i,texture='cube_tex_test.png')
            e.ok = False
            common.cube_list.append(e)
