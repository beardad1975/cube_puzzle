
PHOTO_STAGE = 'photo'
PUZZLE_STAGE = 'puzzle'

PHOTO_WIDTH = 1280
PHOTO_HEIGHT = 720

# capture photo size 720x720
CAP_LEFT_TOP = (280, 0)
CAP_RIGHT_BOTTOM = (280+720, 0+720)

state = PHOTO_STAGE

# opencv
cap = None # video capture

# ursina
app = None
photo_quad = None
photo_tex = None
