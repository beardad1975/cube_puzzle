
from ursina import *
from panda3d.core import Texture
import numpy as np
import cv2

import common 
import capture
import state
from puzzle_camera import PuzzleCamera

def ursina_init():
    # ursina
    common.app = Ursina()
    window.borderless = False
    window.fps_counter.enabled = False
    Text.default_font = 'msjh.ttc'
    Text.default_resolution = 1080 * Text.size
    
    common.puzzle_camera = PuzzleCamera(enabled=False)
    
    common.environment = Entity(model='face_inner_sphere',
                                texture='environment.jpg',
                                scale=10,enable=False)    
    
    common.title_logo = Entity(
        parent = camera.ui,
        model = 'quad',
        scale = (1.2, 0.5),
        texture = 'title_logo.png',
        y = 0.1,
        #color = color.white,
        enabled = False,
        )
    common.title_press_info = Entity(
        parent = camera.ui,
        model = 'quad',
        scale = (0.8, 0.1),
        texture = 'title_press_info.png',
        y = -0.25,
        #color = color.white,
        enabled = False,
        )
    
    common.menu_logo = Entity(
        parent = camera.ui,
        model = 'quad',
        scale = (0.6, 0.15),
        texture = 'menu_logo.png',
        y = 0.3,
        #color = color.white,
        enabled = False,
        )
    
    common.menu_easy_btn = Entity(
        parent = camera.ui,
        model = 'quad',
        
        texture = 'menu_easy_btn.png',

        #color = color.white,
        enabled = False,
        )

    common.menu_hard_btn = Entity(
        parent = camera.ui,
        model = 'quad',
        
        texture = 'menu_hard_btn.png',

        #color = color.white,
        enabled = False,
        )

    common.easy_mode = Entity(
        parent = camera.ui,
        model = 'quad',
        position = (0.5, 0.5, 0 ) ,
        texture = 'easy_mode.png',
        enabled = False,
        )

    common.hard_mode = Entity(
        parent = camera.ui,
        model = 'quad',
        position = (0.7, 0.4, 0 ) ,
        scale = (0.15, 0.15, 0),
        texture = 'hard_mode.png',
        enabled = False,
        )


    common.photo_tex = Texture()
    common.photo_tex.setup2dTexture(common.PHOTO_WIDTH, common.PHOTO_HEIGHT,
                                  Texture.T_unsigned_byte, Texture.F_rgb8)
    common.photo_quad = Entity(
        parent = camera.ui,
        model = 'quad',
        scale_x = window.aspect_ratio,
        #color = color.white,
        enabled = False,
        #z=.02,
        )
    common.photo_info = Entity(
        parent = camera.ui,
        model = 'quad',
        scale = (0.2,0.6,1),
        #color = color.white,
        texture = 'photo_info.png',
        enabled = False,
        position=(-0.7,0.1,0),
        )

    common.photo_white = Entity(
        parent = camera.ui,
        model = 'quad',
        scale_x = window.aspect_ratio,
        color = color.white,
        enabled = False,
        #z=.02,
        )

     
    common.photo_counter = Text('3',color=color.rgba(255,0,0,255),
                            origin=(0,0),position=(-0.05,0,0), enabled=False)

    #common.info = Text(position=window.top_left)

    common.making_logo = Entity(
        parent = camera.ui,
        model = 'quad',
        scale = (0.2,0.7,1),
        #color = color.white,
        texture = 'making_logo.png',
        enabled = False,
        position=(-0.7,0.1,0),
        )

    common.random_logo = Entity(
        parent = camera.ui,
        model = 'quad',
        scale = (0.2,0.7,1),
        #color = color.white,
        texture = 'random_logo.png',
        enabled = False,
        position=(-0.7,0.1,0),
        )

    # load inadvance
    e = Entity(model='cube_puzzle', enabled=False)
    common.cube_list.append(e)

def main():
    
    capture.init()
    ursina_init()
    state.init()
        
    common.app.run()

def update():
    common.current_update()
    
#     if common.state == common.PHOTO_STAGE:
#         capture.update_texture()
#     else:
#         pc = common.puzzle_camera
#         common.info.text = f"rotation_y {pc.rotation_y:.1f}\nrotation_x {pc.rotation_x:.1f}"
        

 


def input(key):
    common.current_input(key)
    
#     if common.state == common.PHOTO_STAGE and key == 'space':
#         common.state = common.MAKING_STAGE
#         common.msg_text.text = '拍照\n完成'
#         common.photo_quad.visible = False
#         capture.make_cube_texture()
#         common.puzzle_camera.enabled = True
#     elif common.state != common.PHOTO_STAGE and key in common.up_turn_keymap:
#         index = common.up_turn_keymap[key]- 1
#         do_up_turn(index)
# 
#     elif common.state != common.PHOTO_STAGE and key in common.right_turn_keymap:
#         index = common.right_turn_keymap[key] - 1
#         do_right_turn(index)
#    
# 
#     elif common.state != common.PHOTO_STAGE and key == 'a':
#         if common.level == common.MEDIUM_LEVEL:
#             do_up_turn(common.target_cube_index)
# 
#     elif common.state != common.PHOTO_STAGE and key == 'b':
#         if common.level == common.MEDIUM_LEVEL:
#             do_right_turn(common.target_cube_index)
# 
#     elif key == 'escape':
#         application.quit()

#     else:
#         pass
#         #print(key)



if __name__ == '__main__':
    main()