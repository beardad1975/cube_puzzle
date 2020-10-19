
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

    common.msg_text = Text('準備\n拍照',color=color.red, scale=5, background=False,
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
    can_animate = False
    
    if common.state == common.PHOTO_STAGE and key == 'space':
        common.state = common.MAKING_STAGE
        common.msg_text.text = '拍照\n完成'
        common.photo_quad.visible = False
        capture.make_cube_texture()
    elif common.state != common.PHOTO_STAGE and key in common.up_turn_keymap:
        index = common.up_turn_keymap[key]- 1
        if index < len(common.cube_list):
            cube = common.cube_list[index]
            try:
                if cube.animations[-1].finished:
                    can_animate = True
            except IndexError:
                # empty list
                can_animate = True  
            
            if can_animate:
                cube.animate_rotation_x(cube.rotation_x + 90 ,duration=0.4)
    elif common.state != common.PHOTO_STAGE and key in common.right_turn_keymap:
        index = common.right_turn_keymap[key] - 1
        if index < len(common.cube_list):
            cube = common.cube_list[index]
            try:
                if cube.animations[-1].finished:
                    can_animate = True
            except IndexError:
                # empty list
                can_animate = True  
            
            if can_animate:
                cube.animate_rotation_y(cube.rotation_y - 90 ,duration=0.4)        


    elif key == 'escape':
        application.quit()
    else:
        print(key)



if __name__ == '__main__':
    main()