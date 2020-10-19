
from ursina import *
from panda3d.core import Texture
import numpy as np
import cv2

import common 
import capture

def init():
    
    capture.init()
    
    # ursina
    common.app = Ursina()
    Text.default_font = 'msjh.ttc'

    common.photo_tex = Texture()
    
    common.photo_tex.setup2dTexture(common.PHOTO_WIDTH, common.PHOTO_HEIGHT,
                                  Texture.T_unsigned_byte, Texture.F_rgb8)

    common.photo_quad = Entity(
        parent = camera.ui,
        model = 'quad',
        scale_x = window.aspect_ratio,
        color = color.white,
        
        )

    common.msg_text = Text('準備\n拍照',color=color.red, scale=5, background=True,
                           x=-0.5*window.aspect_ratio, y=0.1)



def main():
    #print('aspect: ', window.aspect_ratio)
    init()
    
    
    EditorCamera()
    
    common.app.run()

def update():
    if common.state == common.PHOTO_STAGE:
        capture.update_texture()


def input(key):
    pass



if __name__ == '__main__':
    main()