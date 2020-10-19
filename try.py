from ursina import *

app = Ursina()

Entity(model='cube_puzzle', texture='cube_tex_test')

EditorCamera()

app.run()