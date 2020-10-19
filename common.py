
# constants
PHOTO_STAGE = 'photo'
MAKING_STAGE = 'making puzzle'
PUZZLE_STAGE = 'puzzle'


PHOTO_WIDTH = 1280
PHOTO_HEIGHT = 720

BEGINNER_LEVEL = 'beginner' # 2x2
MEDIUM_LEVEL = 'medium'     # 3x3
ADVANCED_LEVEL = 'advanced' # 4x4


# capture photo size 720x720
CAP_LEFT_TOP = (280, 0)
CAP_RIGHT_BOTTOM = (280+720, 0+720)

TEX_SIZE_3X3 = 240  # 720 // 3

# game data

state = PHOTO_STAGE
level = MEDIUM_LEVEL

# opencv data 
cap = None # video capture
buf = None # video buffer



# ursina data
app = None
photo_quad = None
photo_tex = None
cube_list = []
cube_tex_list = []




