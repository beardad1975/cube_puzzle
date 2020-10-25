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
               'random',
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

        self.pressed = False

    def menu_update(self):
        #print('menu update')
        common.puzzle_camera.rotation_y += 0.04
        common.puzzle_camera.rotation_x += math.sin(time.time()*0.5)*0.1

    def menu_input(self, key):
        #print('menu input')
        if key == 'a' and not self.pressed:
            self.pressed = True
            common.menu_hard_btn.enabled = False
            common.level = common.EASY_LEVEL
            easy_btn = common.menu_easy_btn
            #easy_btn.shake()
            easy_btn.animate('position', (0,-0.1,0), duration=0.5)
            easy_btn.animate('scale', (0.45,0.45,1), duration=0.5)
            invoke(self.next_state,delay=1.2)
        elif key == 'b' and not self.pressed:
            self.pressed = True
            common.menu_easy_btn.enabled = False
            common.level = common.HARD_LEVEL
            hard_btn = common.menu_hard_btn
            #hard_btn.shake()
            hard_btn.animate('position', (0,-0.1,0), duration=0.5)
            hard_btn.animate('scale', (0.45,0.45,1), duration=0.5)
            invoke(self.next_state,delay=1.2)

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
        common.photo_quad.color = color.rgba(255,255,255,0)
        common.photo_quad.fade_in(duration=0.5)
        
        common.photo_info.enabled = True
        common.photo_info.color = color.rgba(255,255,255,0)
        common.photo_info.fade_in(duration=0.5)
        
        if common.level == common.HARD_LEVEL :
            common.hard_mode.enabled = True
            common.hard_mode.color = color.rgba(255,255,255,0)
            common.hard_mode.fade_in(duration=0.5)
        
        common.photo_counter.enabled = True
        common.photo_counter.color = color.rgba(255,255,255,0)
        
        
        self.last_time = time.time()
        self.counter = 3
    
    def photo_update(self):
        capture.update_texture()
        now = time.time()
        if now - self.last_time > 1.2:
            print('count')
            self.last_time = now
            common.photo_counter.color = color.rgba(255,0,0,255)
            common.photo_counter.scale = 16
            common.photo_counter.text = str(self.counter)
            common.photo_counter.fade_out(duration=1)
            common.photo_counter.animate_scale(32, duration=1)
            self.counter -= 1
            if self.counter < 0:
                self.next_state()
                
    def photo_input(self, key):
        pass
    
    def on_exit_photo(self):
        print('exit photo ')
        common.photo_quad.enabled = False
        common.photo_info.enabled = False
        common.photo_counter.enabled = False
        common.hard_mode.enabled = False

    # ---------state : making---------
    def on_enter_making(self):
        print('enter making')
        common.current_update = self.making_update
        common.current_input = self.making_input
        
        common.photo_quad.enabled = True
        common.photo_white.enabled = True
        common.photo_white.color = color.white
        common.photo_white.fade_out(duration=1)

        def show_logo():
            common.making_logo.enabled=True
            common.making_logo.shake(duration=1.6)
        invoke(show_logo, delay=2) 
        invoke(self.next_state, delay=3.6)

        #common.hard_mode.enabled = True
        #common.making_logo.enabled = True
        #self.last_time = time.time()
    
    def making_update(self):
        pass
        #now = time.time()
        #if now - self.last_time > 2:
       
    def making_input(self, key):
        pass
    
    def on_exit_making(self):
        print('exit making ')
        common.photo_quad.enabled = False
        common.photo_white.enabled = False
        common.making_logo.enabled= False
        if common.level == common.HARD_LEVEL:
            capture.make_cube_texture3x3()

    # ---------state : random---------
    def on_enter_random(self):
        print('enter random')
        common.current_update = self.random_update
        common.current_input = self.random_input
        
        common.environment.enabled = True
        common.puzzle_camera.position = 0,0,0
        common.puzzle_camera.rotation = 0,0,0
        if common.level == common.HARD_LEVEL :
            common.hard_mode.enabled = True
            common.hard_mode.color = color.rgba(255,255,255,0)
            common.hard_mode.fade_in(duration=0.5)
    
    def random_update(self):
        pc = common.puzzle_camera
        now = time.time()
        pc.rotation_x = math.sin(now*0.3) * 15
        pc.rotation_y = math.cos(now*0.3) * 15
    
    def random_input(self, key):
        pass
    
    def on_exit_random(self):
        print('exit random')
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
