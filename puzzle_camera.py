from ursina import *
import common

class PuzzleCamera(Entity):

    def __init__(self, **kwargs):
        camera.editor_position = (0,0,-10)
        super().__init__(name='puzzle_camera', eternal=True)

        self.rotation_speed = 200
        self.pan_speed = Vec2(5, 5)
        self.move_speed = 10
        self.zoom_speed = .75
        self.rotate_around_mouse_hit = False

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.start_position = self.position
        self.perspective_fov = camera.fov
        self.orthographic_fov = camera.fov
        self.on_destroy = self.on_disable


    def on_enable(self):
        camera.org_parent = camera.parent
        camera.org_position = camera.position
        camera.org_rotation = camera.rotation

        camera.parent = self
        camera.position = camera.editor_position
        camera.rotation = (0,0,0)


    def on_disable(self):
        camera.editor_position = camera.position
        camera.parent = camera.org_parent
        camera.position = camera.org_position
        camera.rotation = camera.org_rotation


    def input(self, key):
#         if key == 'p':
#             if not camera.orthographic:
#                 self.orthographic_fov = camera.fov
#                 camera.fov = self.perspective_fov
#             else:
#                 self.perspective_fov = camera.fov
#                 camera.fov = self.orthographic_fov
# 
#             camera.orthographic = not camera.orthographic

#         if key == 'f':
#             self.position = self.start_position

        if key == 'scroll up' and not held_keys['control']:
            if not camera.orthographic:
                target_position = Vec3(0,0,0)
                if mouse.hovered_entity and not mouse.hovered_entity.has_ancestor(camera):
                    target_position = mouse.hovered_entity.world_position

                camera.world_position = lerp(camera.world_position, target_position, self.zoom_speed * time.dt * 10)
            else:
                camera.fov -= self.zoom_speed * 100 * time.dt

        elif key == 'scroll down' and not held_keys['control']:
            if not camera.orthographic:
                camera.world_position += camera.back * self.zoom_speed * 100 * time.dt
            else:
                camera.fov += self.zoom_speed * 100 * time.dt

#         elif key == 'right mouse down' or key == 'middle mouse down':
#             if mouse.hovered_entity and self.rotate_around_mouse_hit:
#                 org_pos = camera.world_position
#                 self.world_position = mouse.world_point
#                 camera.world_position = org_pos


#         elif key == 'a':
#             print(camera.world_position)

    def update(self):
#         if held_keys['right arrow']:
#             #print(self.rotation_y)
#             if common.level == common.MEDIUM_LEVEL:
#                 if self.rotation_y < common.rot_y_linspace3x3[-1]:
#                     self.rotation_y += 40 * time.dt
#                     calc_target_and_update3x3()
#         elif held_keys['left arrow']:
#             if common.level == common.MEDIUM_LEVEL:
#                 if self.rotation_y > common.rot_y_linspace3x3[0]:
#                     self.rotation_y -= 40 * time.dt
#                     calc_target_and_update3x3()
#         elif held_keys['down arrow']:
#             if common.level == common.MEDIUM_LEVEL:
#                 if self.rotation_x < common.rot_x_linspace3x3[-1]:
#                     self.rotation_x += 40 * time.dt
#                     calc_target_and_update3x3()
#         elif held_keys['up arrow']:
#             if common.level == common.MEDIUM_LEVEL:
#                 if self.rotation_x > common.rot_x_linspace3x3[0]:
#                     self.rotation_x -= 40 * time.dt
#                     calc_target_and_update3x3()
        
        if mouse.right:
            self.rotation_x -= mouse.velocity[1] * self.rotation_speed
            self.rotation_y += mouse.velocity[0] * self.rotation_speed

#             self.position += camera.right * held_keys['d'] * (self.move_speed + (self.move_speed * held_keys['shift']) - (self.move_speed*.9 * held_keys['alt'])) * time.dt
#             self.position += camera.left * held_keys['a'] * (self.move_speed + (self.move_speed * held_keys['shift']) - (self.move_speed*.9 * held_keys['alt'])) * time.dt
#             self.position += camera.forward * held_keys['w'] * (self.move_speed + (self.move_speed * held_keys['shift']) - (self.move_speed*.9 * held_keys['alt'])) * time.dt
#             self.position += camera.back * held_keys['s'] * (self.move_speed + (self.move_speed * held_keys['shift']) - (self.move_speed*.9 * held_keys['alt'])) * time.dt
#             self.position += camera.up * held_keys['e'] * (self.move_speed + (self.move_speed * held_keys['shift']) - (self.move_speed*.9 * held_keys['alt'])) * time.dt
#             self.position += camera.down * held_keys['q'] * (self.move_speed + (self.move_speed * held_keys['shift']) - (self.move_speed*.9 * held_keys['alt'])) * time.dt


        if mouse.middle:
            self.position -= camera.right * mouse.velocity[0] * self.pan_speed[0]
            self.position -= camera.up * mouse.velocity[1] * self.pan_speed[1]




# def calc_target_and_update3x3():
#     # calc col index
#     pc = common.puzzle_camera
#     
#     if pc.rotation_y <= common.rot_y_linspace3x3[1]:
#         col = 2
#     elif pc.rotation_y >= common.rot_y_linspace3x3[2]:
#         col = 0
#     else: # in between
#         col = 1
#     
#     # calc row index
#     if pc.rotation_x >= common.rot_y_linspace3x3[2]:
#         row = 0
#     elif pc.rotation_x <= common.rot_y_linspace3x3[1]:
#         row = 2
#     else: # in between
#         row = 1    
#     
#     index = row*3 + col
#     #print('index ', index)
#     # check and update
#     if index != common.target_cube_index:
#         common.target_cube_index = index
#         for i,c in enumerate(common.cube_list):
#             if i == index:
#                 c.animate_z(-0.2,duration=.2)
#                 
#             else:
#                 c.animate_z(0,duration=.2)
                



if __name__ == '__main__':
    # window.vsync = False
    app = Ursina()
    '''
    Simple camera for debugging.
    Hold right click and move the mouse to rotate around point.
    '''

    sky = Sky()
    e = Entity(model='cube', color=color.white)
    e.model.colorize()

    from ursina.prefabs.first_person_controller import FirstPersonController
    from copy import copy
    # player = FirstPersonController()
    # Entity(parent=player, model='cube', color=color.orange, scale_y=2, origin_y=0)
    ground = Entity(model='plane', scale=32, texture='white_cube', texture_scale=(32,32))
    box = Entity(model='cube', collider='box', texture='white_cube', scale=(10,2,2), position=(2,1,5), color=color.light_gray)
    ec = EditorCamera(rotation_smoothing=2, enabled=True, rotation=(30,30,0))

    rotation_info = Text(position=window.top_left)

    def update():
        rotation_info.text = str(int(ec.rotation_y)) + '\n' + str(int(ec.rotation_x)) 

    def input(key):
        if key == 'tab':    # press tab to toggle edit/play mode
            # player.ignore = not player.ignore
            ec.enabled = not ec.enabled

    app.run()
