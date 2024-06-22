from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController as FPC
from ursina.shaders import basic_lighting_shader as lit

app = Ursina()
sky = Sky(color=color.light_gray)
shader = lit
player = FPC()
ground = Entity(model='plane',texture="/assets/textures/pooltile.png",collider='mesh',position=(0,-2,0),
                scale=(50,4,50))
box = Entity(model='cube',texture='/assets/textures/tile',position=(1,0,1),collider='box',scale=(2,2,2))
lightbulb = Entity(model='cube',texture='/assets/textures/tile',position=(4,3,1),collider='box',scale=(2,2,2),color=rgb(0,200,200))
app.run()