from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController as FPC
from ursina.shaders import colored_lights_shader as lit

app = Ursina()
player = FPC()
ground = Entity(model='plane',texture="/assets/textures/tile.png",collider='mesh',position=(0,-2,0),
                scale=(50,4,50))
box = Entity(model='cube',texture='/assets/textures/tile',position=(1,0,1),collider='box',scale=(2,2,2),
             shader=lit)
lightbulb = Entity(model='cube',texture='/assets/textures/tile',position=(4,3,1),collider='box',scale=(2,2,2))
lighting = DirectionalLight(parent=lightbulb, shadows=True)

app.run()