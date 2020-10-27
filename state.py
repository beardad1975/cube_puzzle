import math
import time
import random

from ursina import *

from transitions import Machine

import common
import capture
import control


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
        
    #  dummy
    def dummy_update(self):
        pass
    
    def dummy_input(self, key):
        pass

    
    # ---------state : title---------
    def on_enter_title(self):
        print('enter title')
        # update and input
        common.success = False
        
        common.current_update = self.title_update
        common.current_input = self.title_input
        
        capture.clean_cube_and_img()
        
        
        #camera.editor_position
        
        # handle delayed show up logo
        common.button_a.enabled = False
        common.button_b.enabled = False
        common.puzzle_logo.enabled = False
        common.hard_mode.enabled = False
        common.puzzle_countdown_info.enabled = False
        
        # entity
        common.environment.enabled = True
        
        common.title_logo.enabled = True
        common.title_logo.color = color.rgba(255,255,255,0)
        common.title_logo.fade_in(duration=2)
        
        common.title_press_info.enabled = True
        
        
        # camera
        common.puzzle_camera.enabled = True
        camera.position = Vec3(0,0,-35)
        camera.rotation = Vec3(0,0,0)
        
        #
        self.pressed = False

    def title_update(self):
        #print('update title')
        #common.puzzle_camera.rotation_y += 0.03
        #common.puzzle_camera.rotation_x += math.sin(time.time()*0.3)*0.1

        a, b = control.control_camera_return_ab()
        if not self.pressed:
            if a or b:
                self.pressed = True
                self.next_state()
                

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
        
        camera.position = camera.editor_position
        

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

        self.pressed = True
        def press_enable():
            self.pressed = False
        invoke(press_enable, delay=1)



    def menu_update(self):
        #print('menu update')
        common.puzzle_camera.rotation_y += 0.04
        common.puzzle_camera.rotation_x += math.sin(time.time()*0.5)*0.1

        a, b = control.return_ab()
        if a and not self.pressed:
            self.pressed = True
            common.menu_hard_btn.enabled = False
            common.level = common.EASY_LEVEL
            easy_btn = common.menu_easy_btn
            #easy_btn.shake()
            easy_btn.animate('position', (0,-0.1,0), duration=0.5)
            easy_btn.animate('scale', (0.45,0.45,1), duration=0.5)
            invoke(self.next_state,delay=1.2)
        elif b and not self.pressed:
            self.pressed = True
            common.menu_easy_btn.enabled = False
            common.level = common.HARD_LEVEL
            hard_btn = common.menu_hard_btn
            #hard_btn.shake()
            hard_btn.animate('position', (0,-0.1,0), duration=0.5)
            hard_btn.animate('scale', (0.45,0.45,1), duration=0.5)
            invoke(self.next_state,delay=1.2)

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
        else:
            common.easy_mode.enabled = True
            common.easy_mode.color = color.rgba(255,255,255,0)
            common.easy_mode.fade_in(duration=0.5)
            
        
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
        common.easy_mode.enabled = False

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
            common.making_logo.shake(duration=1)
        invoke(show_logo, delay=1.5) 
        invoke(self.next_state, delay=2.5)

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
        else:
            capture.make_cube_texture2x2()

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
        else:
            common.easy_mode.enabled = True
            common.easy_mode.color = color.rgba(255,255,255,0)
            common.easy_mode.fade_in(duration=0.5)
            # a little zoom camera
            camera.world_position = lerp(camera.world_position, Vec3(0,0,0), 0.3)
        
        
        if common.level == common.HARD_LEVEL:
            self.random_gen3x3()
        else:
            self.random_gen2x2()

        # add ok attr on cubes (must befor random turn)
        for c in common.cube_list:
            c.ok = False
        
        self.can_random = False
        
        def show_logo():
            common.random_logo.enabled = True
            common.random_logo.color = color.rgba(255,255,255,0)
            common.random_logo.fade_in(duration=0.5)
            #self.can_random = True
        
        def start_random():
            self.can_random = True
        
        invoke(show_logo, delay=1.5)
        invoke(start_random, delay=3.5)
        
    def random_gen3x3(self):
        self.random_steps = []
        for i in range(9):
            rand_num = random.randint(1,7)
            tmp1 = [(i, 'up')] * rand_num
            #for r in range(rand_num):
            #    self.random_steps.append((i, do_up_turn))
            
            rand_num = random.randint(1,4)
            tmp2 = [(i, 'right')] * rand_num
            #for r in range(rand_num):
            #    self.random_steps.append((i, do_right_turn))

            rand_num = random.randint(1,4)
            tmp3 = [(i, 'left')] * rand_num
            #for r in range(rand_num):
            #    self.random_steps.append((i, do_left_turn))
            self.random_steps = self.random_steps + tmp1 + tmp2 + tmp3
            
        random.shuffle(self.random_steps)

    def random_gen2x2(self):
        self.random_steps = []
        for i in range(4):
            rand_num = random.randint(1,7)
            tmp1 = [(i, 'up')] * rand_num
            #for r in range(rand_num):
            #    self.random_steps.append((i, do_up_turn))
            
            rand_num = random.randint(1,4)
            tmp2 = [(i, 'right')] * rand_num
            #for r in range(rand_num):
            #    self.random_steps.append((i, do_right_turn))

            rand_num = random.randint(1,4)
            tmp3 = [(i, 'left')] * rand_num
            #for r in range(rand_num):
            #    self.random_steps.append((i, do_left_turn))
            self.random_steps = self.random_steps + tmp1 + tmp2 + tmp3
            
        random.shuffle(self.random_steps)


    def random_update(self):
        #print('here')
        pc = common.puzzle_camera
        now = time.time()
        pc.rotation_x = math.sin(now*0.3) * 15
        pc.rotation_y = math.cos(now*0.3) * 15
    
        if self.can_random and len(self.random_steps):
            index, move = self.random_steps[-1]

            ret = False
            if move == 'up':
                ret = do_up_turn(index, duration=0.2)
            elif move == 'right':
                ret = do_right_turn(index, duration=0.2)
            elif move == 'left':
                ret = do_left_turn(index, duration=0.2)
            
            #ret = callee(index, duration=0.2)
            if ret:
                self.random_steps.pop()
        elif self.can_random and not len(self.random_steps):
            pass
            # next state            
            self.next_state()
        
    
    def random_input(self, key):
        pass
    
    def on_exit_random(self):
        print('exit random')
        common.random_logo.enabled = False
        common.hard_mode.enabled = False
        common.easy_mode.enabled = False
        self.can_random = False

    # ---------state : puzzle---------
    def on_enter_puzzle(self):
        print('enter puzzle')
        
        common.current_update = self.dummy_update
        common.current_input = self.dummy_input
        
        common.puzzle_logo.enabled = True
        common.puzzle_logo.color = color.rgba(255,255,255,255)
        common.puzzle_logo.scale = (0.6, 0.15,1)
        common.puzzle_logo.animate_scale((1.8 , 0.45, 1), duration=1)
        common.puzzle_logo.fade_out(duration=1)

        if common.level == common.HARD_LEVEL :
            common.hard_mode.enabled = True
            self.puzzle_countdown = common.HARD_TIME_LIMIT
        else:
            common.easy_mode.enabled = True
            self.puzzle_countdown = common.EASY_TIME_LIMIT

        def start_puzzle():
            #print('start puzzle')
            common.current_update = self.puzzle_update
            common.current_input = self.puzzle_input
            common.button_a.enabled = True
            common.button_b.enabled = True
            self.last_time = time.time()
            self.check_time = time.time()
            
            common.puzzle_countdown_info.enabled = True
            common.puzzle_countdown_info.text = str(self.puzzle_countdown)
            #check ok
            self.ok_counter = 0
            self.check_cubes()
        invoke(start_puzzle, delay=1.5)
    
    
    
    def puzzle_update(self):
        now = time.time()
        # countdown time
        if now - self.last_time > 1:
            self.last_time = now
            self.puzzle_countdown -= 1
            common.puzzle_countdown_info.text = str(self.puzzle_countdown)
            if self.puzzle_countdown == 0:
                common.success = False
                self.next_state()
        # check time
        if now - self.check_time > 0.05:
            self.check_time = now
            self.check_cubes()
        
        # 
        a, b = control.control_cube_return_ab()
        if a :
            do_up_turn(common.target_cube_index)
        if b :
            do_right_turn(common.target_cube_index)
        
        pc = common.puzzle_camera
        if held_keys['right arrow']:
            #print(self.rotation_y)
            if common.level == common.HARD_LEVEL:
                if pc.rotation_y < common.rot_y_linspace3x3[-1]:
                    pc.rotation_y += 40 * time.dt
                    self.calc_target_and_update3x3()
            else:
                if pc.rotation_y < common.rot_y_linspace2x2[-1]:
                    pc.rotation_y += 40 * time.dt
                    self.calc_target_and_update2x2()
        elif held_keys['left arrow']:
            if common.level == common.HARD_LEVEL:
                if pc.rotation_y > common.rot_y_linspace3x3[0]:
                    pc.rotation_y -= 40 * time.dt
                    self.calc_target_and_update3x3()
            else:
                if pc.rotation_y > common.rot_y_linspace2x2[0]:
                    pc.rotation_y -= 40 * time.dt
                    self.calc_target_and_update2x2()                
        elif held_keys['down arrow']:
            if common.level == common.HARD_LEVEL:
                if pc.rotation_x < common.rot_x_linspace3x3[-1]:
                    pc.rotation_x += 40 * time.dt
                    self.calc_target_and_update3x3()
            else:
                if pc.rotation_x < common.rot_x_linspace2x2[-1]:
                    pc.rotation_x += 40 * time.dt
                    self.calc_target_and_update2x2()
        elif held_keys['up arrow']:
            if common.level == common.HARD_LEVEL:
                if pc.rotation_x > common.rot_x_linspace3x3[0]:
                    pc.rotation_x -= 40 * time.dt
                    self.calc_target_and_update3x3()
            else:
                if pc.rotation_x > common.rot_x_linspace2x2[0]:
                    pc.rotation_x -= 40 * time.dt
                    self.calc_target_and_update2x2()

    def calc_target_and_update3x3(self):
        # calc col index
        pc = common.puzzle_camera
        
        if pc.rotation_y <= common.rot_y_linspace3x3[1]:
            col = 2
        elif pc.rotation_y >= common.rot_y_linspace3x3[2]:
            col = 0
        else: # in between
            col = 1
        
        # calc row index
        if pc.rotation_x >= common.rot_y_linspace3x3[2]:
            row = 0
        elif pc.rotation_x <= common.rot_y_linspace3x3[1]:
            row = 2
        else: # in between
            row = 1    
        
        index = row*3 + col
        #print('index ', index)
        # check and update
        if index != common.target_cube_index:
            common.target_cube_index = index
            for i,c in enumerate(common.cube_list):
                if i == index:
                    c.animate_z(-0.3,duration=.2)
                    
                else:
                    c.animate_z(0,duration=.2)

    def calc_target_and_update2x2(self):
        # calc col index
        pc = common.puzzle_camera
        
        if pc.rotation_y <= common.rot_y_linspace2x2[1]:
            col = 1

        else: 
            col = 0
        
        # calc row index
        if pc.rotation_x >= common.rot_y_linspace2x2[1]:
            row = 0
        else: # in between
            row = 1    
        
        index = row*2 + col
        #print('index ', index)
        # check and update
        if index != common.target_cube_index:
            common.target_cube_index = index
            for i,c in enumerate(common.cube_list):
                if i == index:
                    c.animate_z(-0.3,duration=.2)
                    
                else:
                    c.animate_z(0,duration=.2)


    def puzzle_input(self, key):
        if key == 'a':
            
            ret = do_up_turn(common.target_cube_index)
#             if ret :
#                 invoke(self.check_cubes, delay=0.45)
            

        elif key == 'b':
            
            ret = do_right_turn(common.target_cube_index)
#             if ret:
#                 invoke(self.check_cubes, delay=0.4)
            
            
#         elif key == 'space':
#             self.check_cubes()
#         elif key == 'x':
#             common.cube_list[0].rotation_x = 15
#         elif key == 'y':
#             common.cube_list[0].rotation_y = 15
            
    def check_cubes(self):
        for c in common.cube_list:
            rot = c.rotation
            if not c.ok and abs(rot[0] % 360) < 2 and abs(rot[1] % 360) < 2 and abs(rot[2] % 360) < 2:
                c.ok = True
                self.ok_counter += 1
                c.setTexture(common.ok_ts,common.ok_tex)
        if common.level == common.HARD_LEVEL and self.ok_counter == 9:
            common.success = True
            self.next_state()
        elif common.level == common.EASY_LEVEL and self.ok_counter == 4:
            common.success = True
            self.next_state()

    def on_exit_puzzle(self):
        print('exit puzzle')
        common.button_a.enabled = False
        common.button_b.enabled = False
        common.puzzle_logo.enabled = False
        common.hard_mode.enabled = False
        common.easy_mode.enabled = False
        common.puzzle_countdown_info.enabled = False

    # ---------state : result---------
    def on_enter_result(self):
        print('enter result')
        common.puzzle_camera.rotation_x = 0
        common.puzzle_camera.rotation_y = 0
        # flatten cubes
        for c in common.cube_list:
            c.z = 0
        
        common.current_update = self.result_update
        common.current_input = self.result_input
        if common.success:
            common.success_logo.enabled = True
            
        else:
            common.fail_logo.enabled = True
            
        if common.level == common.HARD_LEVEL :
            common.hard_mode.enabled = True
            
        else:
            common.easy_mode.enabled = True
            
    
    def result_update(self):
        pc = common.puzzle_camera
        now = time.time()
        pc.rotation_x = math.sin(now*0.3) * 15
        pc.rotation_y = math.cos(now*0.3) * 15
    
    def result_input(self, key):
        pass
    
    def on_exit_result(self):
        print('exit result')
        common.success_logo.enabled = False
        common.fail_logo.enabled = False
        common.hard_mode.enabled = False
        common.easy_mode.enabled = False


def init():
    machine = StateAction()
    common.state_machine = machine
    machine.to_title()


    

def do_up_turn(index, duration=0.4):
    can_animate = False
    if index < len(common.cube_list):
        cube = common.cube_list[index]
        try:
            if not cube.ok and cube.animations[-1].finished:
                can_animate = True
        except IndexError:
            # empty list
            can_animate = True  
        
        if can_animate:
            remainder = cube.rotation_x % 90
            if abs(remainder) < 1 :
                remainder = 0            
            cube.animate_rotation_x(cube.rotation_x + 90 - remainder ,duration=duration)
    return can_animate
    
def do_right_turn(index, duration=0.4):
    can_animate = False
    if index < len(common.cube_list):
        cube = common.cube_list[index]
        try:
            if not cube.ok and cube.animations[-1].finished:
                can_animate = True
        except IndexError:
            # empty list
            can_animate = True  
        
        if can_animate:
            remainder = cube.rotation_y % 90
            if abs(remainder) < 1 :
                remainder = 0    
            cube.animate_rotation_y(cube.rotation_y - 90 - remainder ,duration=duration)
    return can_animate

def do_left_turn(index, duration=0.4):
    can_animate = False
    if index < len(common.cube_list):
        cube = common.cube_list[index]
        try:
            if not cube.ok and cube.animations[-1].finished:
                can_animate = True
        except IndexError:
            # empty list
            can_animate = True  
        
        if can_animate:
            remainder = cube.rotation_y % 90
            if abs(remainder) < 1 :
                remainder = 0    
            cube.animate_rotation_y(cube.rotation_y + 90 - remainder ,duration=duration)    

    return can_animate
