# basic setup
#fullscreen = True     # 全螢幕
fullscreen = False
port = 'com46'        # microbit 連接埠
#port = 'com13'
EASY_TIME_LIMIT = 80  # 簡單時間限制
HARD_TIME_LIMIT = 120 # 困難時間限制




# serial data
ser = None
last_x = 0
last_y = 0
last_z = 0


# constants
PHOTO_STAGE = 'photo'
MAKING_STAGE = 'making puzzle'
PUZZLE_STAGE = 'puzzle'


PHOTO_WIDTH = 1280
PHOTO_HEIGHT = 720

EASY_LEVEL = 'easy' # 2x2
HARD_LEVEL = 'hard'     # 3x3

EASY_TIME_LIMIT = 80
HARD_TIME_LIMIT = 120

# EASY_TARGET = 3
# HARD_TARGET = 7


# capture photo size 720x720
CAP_SQUARE_SIZE = 720
CAP_LEFT_TOP = (280, 0)
CAP_RIGHT_BOTTOM = (280+720, 0+720)

TEX_SIZE_3X3 = 240  # 720 // 3
TEX_SIZE_2X2 = 360  # 720 // 2
# game data

state = PHOTO_STAGE
level = EASY_LEVEL
success = False

# opencv data 
cap = None # video capture
buf = None # video buffer




# state machine
state_machine = None
current_update = None
current_input = None

back_title = 0 #  1: for confirm  ,  2: to title state


# ursina data
app = None

puzzle_camera = None

environment = None
title_logo = None
title_press_info = None

menu_logo = None
menu_easy_btn = None
menu_hard_btn = None

easy_mode = None
hard_mode = None

photo_quad = None
photo_tex = None

msg_text = None
info = None

cube_list = []
target_cube_index = 0

cube_img_list = []
cube_border_list = []

# ok texture and texture stage
ok_tex = None
ok_ts = None



rot_y_linspace3x3 = -50, -50+33, -50+33*2, 50
rot_x_linspace3x3 = -50, -50+33, -50+33*2, 50

rot_y_linspace2x2 = -50, 0, 50
rot_x_linspace2x2 = -50, 0, 50



up_turn_keymap = {'1':1,
           '2':2,
           '3':3,
           '4':4,
           '5':5,
           '6':6,
           '7':7,
           '8':8,
           '9':9,
            }

right_turn_keymap = {'q':1,
           'w':2,
           'e':3,
           'r':4,
           't':5,
           'y':6,
           'u':7,
           'i':8,
           'o':9,
            }
