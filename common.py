
# constants
PHOTO_STAGE = 'photo'
MAKING_STAGE = 'making puzzle'
PUZZLE_STAGE = 'puzzle'


PHOTO_WIDTH = 1280
PHOTO_HEIGHT = 720

BEGINNER_LEVEL = 'beginner' # 2x2
MEDIUM_LEVEL = 'medium'     # 3x3



# capture photo size 720x720
CAP_SQUARE_SIZE = 720
CAP_LEFT_TOP = (280, 0)
CAP_RIGHT_BOTTOM = (280+720, 0+720)

TEX_SIZE_3X3 = 240  # 720 // 3

# game data

state = PHOTO_STAGE
level = MEDIUM_LEVEL

# opencv data 
cap = None # video capture
buf = None # video buffer


# state machine
state_machine = None
current_update = None
current_input = None


# ursina data
app = None

title_quad = None

photo_quad = None
photo_tex = None

msg_text = None
info = None

cube_list = []
target_cube_index = 0

cube_img_list = []
cube_border_list = []




rot_y_linspace3x3 = -50, -50+33, -50+33*2, 50
rot_x_linspace3x3 = -50, -50+33, -50+33*2, 50





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
