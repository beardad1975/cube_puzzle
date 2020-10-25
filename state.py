import math
import time

from ursina import *
from transitions import Machine

import common
import capture

class StateAction(Machine):
    def __init__(self):
        states = [ 
               'title',
               'menu',
               'photo', 
               'making',
               'puzzle',
               'result',
             ]
        Machine.__init__(self, states=states, initial='title')
        self.add_ordered_transitions()
        
        
    
    # ---------state : title---------
    def on_enter_title(self):
        print('enter title')
        # update and input
        common.current_update = self.title_update
        common.current_input = self.title_input
        
        # entity
        common.environment.enabled = True
        
        common.title_logo.enabled = True
        common.title_logo.color = color.rgba(255,255,255,0)
        common.title_logo.fade_in(duration=2)
        common.title_press_info.enabled = True
        common.title_press_info.blink(duration=2, loop=True,curve=curve.linear_boomerang)
        
        # camera
        common.puzzle_camera.enabled = True

    def title_update(self):
        #print('update title')
        common.puzzle_camera.rotation_y += 0.04
        common.puzzle_camera.rotation_x += math.sin(time.time()*0.5)*0.1

    def title_input(self, key):
        #print('input title, key:', key)
        if key  in ('a', 'b'):
            self.next_state()

    def on_exit_title(self):
        print('exit title')        
        # entity
        
        #common.title_logo.fade_out(duration=0.5)
        
        #invoke(setattr,args=(common.title_logo, 'enabled',False),delay=1)
        common.title_logo.enabled = False
        
        #common.title_press_info.fade_out(duration=0.5)
        #invoke(setattr,(common.title_press_info, 'enabled',False),delay=1)
        common.title_press_info.enabled = False
        
        

    # ---------state : menu---------
    def on_enter_menu(self):
        print('enter menu')
        common.current_update = self.menu_update
        common.current_input = self.menu_input

        common.environment.enabled = True
        
        common.menu_logo.enabled = True
        common.menu_logo.color = color.rgba(255,255,255,0)
        common.menu_logo.fade_in(duration=0.5)
        
        common.menu_easy_btn.enabled = True
        common.menu_easy_btn.position = -0.25, -0.1, 0
        common.menu_easy_btn.scale = 0.3, 0.3, 1
        common.menu_easy_btn.color = color.rgba(255,255,255,0)
        common.menu_easy_btn.fade_in(duration=0.5)
    
        common.menu_hard_btn.enabled = True
        common.menu_hard_btn.position = 0.25, -0.1 ,0
        common.menu_hard_btn.scale = 0.3, 0.3, 1
        common.menu_hard_btn.color = color.rgba(255,255,255,0)
        common.menu_hard_btn.fade_in(duration=0.5)

    def menu_update(self):
        #print('menu update')
        common.puzzle_camera.rotation_y += 0.04
        common.puzzle_camera.rotation_x += math.sin(time.time()*0.5)*0.1

    def menu_input(self, key):
        #print('menu input')
        if key == 'a':
            common.menu_hard_btn.enabled = False
            common.level = common.EASY_LEVEL
            easy_btn = common.menu_easy_btn
            #easy_btn.shake()
            easy_btn.animate('position', (0,-0.1,0), duration=0.5)
            easy_btn.animate('scale', (0.45,0.45,1), duration=0.5)
            invoke(self.next_state,delay=2)
        elif key == 'b':
            common.menu_easy_btn.enabled = False
            common.level = common.HARD_LEVEL
            hard_btn = common.menu_hard_btn
            #hard_btn.shake()
            hard_btn.animate('position', (0,-0.1,0), duration=0.5)
            hard_btn.animate('scale', (0.45,0.45,1), duration=0.5)
            invoke(self.next_state,delay=2)

    def on_exit_menu(self):
        print('exit menu ')
        common.menu_logo.enabled = False
        common.menu_easy_btn.enabled = False
        common.menu_hard_btn.enabled = False
        common.environment.enabled = False

    # ---------state : photo---------
    def on_enter_photo(self):
        print('enter photo')
        common.current_update = self.photo_update
        common.current_input = self.photo_input
        
        common.photo_quad.enabled = True
        common.photo_info.enabled = True
        
        if common.level == common.HARD_LEVEL :
            common.hard_mode.enabled = True
        
        pass
    
    def photo_update(self):
        capture.update_texture()
    
    def photo_input(self, key):
        pass
    
    def on_exit_photo(self):
        print('exit photo ')
        pass

    # ---------state : making---------
    def on_enter_making(self):
        print('enter making')
        pass
    
    def making_update(self):
        pass
    
    def making_input(self, key):
        pass
    
    def on_exit_making(self):
        print('exit making ')
        pass

    # ---------state : puzzle---------
    def on_enter_puzzle(self):
        print('enter puzzle')
        pass
    
    def puzzle_update(self):
        pass
    
    def puzzle_input(self, key):
        pass
    
    def on_exit_puzzle(self):
        print('exit puzzle')
        pass

    # ---------state : result---------
    def on_enter_result(self):
        print('enter result')
        pass
    
    def result_update(self):
        pass
    
    def result_input(self, key):
        pass
    
    def on_exit_result(self):
        print('exit result')
        pass



def init():
    machine = StateAction()
    common.state_machine = machine
    machine.to_title()
