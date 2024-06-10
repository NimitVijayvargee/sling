from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
floor = Entity(model='cube', scale=(10,1,10), position=(0,-10,0), collider='box',texture='/assets/textures/tile.png')
def update():
    if held_keys['escape']:
        quit()


gun = Button(parent=scene, model='/assets/models/gun/ump45',  origin_y=-.5, position=(3,0,3), collider='box')
def get_gun():
    gun.parent = camera
    gun.position = Vec3(.5,-.6,.5)
    gun.scale = (0.3,0.3,0.3)
    gun.rotation = (0,270,0)
    player.gun = gun

player = FirstPersonController()
player.gun = None
gun.on_click = get_gun
def input(key):
    if key == 'left mouse down' and player.gun:
        gun.rotation = (0,270,20)
        gun.rotation = (0,0,0)
        bullet = Entity(parent=gun, model='cube', scale=.1, color=color.black, position=(-0.3,0.3,0.3))
        bullet.world_parent = scene
        bullet.animate_position(bullet.position+(bullet.forward*100), curve=curve.in_expo, duration=0.3)
        gun.rotation = (0,270,0)
        destroy(bullet, delay=1)
        gun.rotation = (0,270,0)

hookshot_target = Button(parent=scene, model='cube', color=color.brown, position=(4,5,5))
hookshot_target.on_click = Func(player.animate_position, (hookshot_target.x, hookshot_target.y-2,hookshot_target.z), duration=.5, curve=curve.linear)


app.run()