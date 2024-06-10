from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
from ursina.prefabs.sky import Sky
from ursina.prefabs.trail_renderer import TrailRenderer
ammo = 0
app = Ursina(borderless=False,title='Sling')
window.exit_button.visible = False

sky = Sky()
floor = Entity(model='cube', scale=(10,1,10), position=(0,-10,0), collider='box',texture='/assets/textures/tile.png')
reloading = False

def shoot():
    global ammo
    ammo -= 1
    gun.rotation = (0,0,0)
    bullet = Entity(parent=gun, model='cube', scale=(.1,.1,.5), color=color.black, position=(-0.3,1.5,0.3), collider='box')
    bullet.world_parent = scene
    bullet.animate_position(bullet.position+(bullet.forward*1000), curve=curve.linear, duration=4) #big number bullet far :O
    invoke(TrailRenderer,size=[.1,.1], segments=2, min_spacing=.05, fade_speed=1, parent=bullet, color_gradient=[color.yellow, color.white], delay=0.3 )
    gun.rotation = (0,270,0)
    destroy(bullet, delay=3)

def update():
    global reloading
    global ammo
    info.text = f"HP: {player.hp}/100 \nAmmo:{ammo}/40"
    if held_keys['-'] and player.hp is not 0:
        player.hp -= 1
    if held_keys['='] and player.hp is not 100:
        player.hp += 1
    if player.hp is 0:
        info.text = "rip bozo you dead"
        time.sleep(3)
        quit()
    if held_keys['escape']:
        quit()
    if held_keys['r']:
        if player.gun and not reloading:
            Audio(sound_file_name='/assets/soundfiles/reload.mp3')
            reloading=True
            reload()
    if not held_keys['r']:
        reloading = False

    if mouse.left and player.gun: 
        if ammo < 1:
            return None
        else:
            shoot()
            Wait(1)
        

def reload():
    global ammo
    ammo = 40

gun = Button(parent=scene, model='/assets/models/gun/ump45',  origin_y=-.5, position=(3,0,3), collider='box', color=color.black)
def get_gun():
    gun.parent = camera
    gun.position = Vec3(.5,-.6,.5)
    gun.scale = (0.3,0.3,0.3)
    gun.rotation = (0,270,0)
    player.gun = gun
    global ammo
    ammo = 40

player = FirstPersonController()
player.gun = None
player.hp = 100
info = Text(text=f"HP: {player.hp}/100 \nAmmo:{ammo}/40")
gun.on_click = get_gun
    

hookshot_target = Button(parent=scene, model='cube', color=color.brown, position=(4,5,5))
hookshot_target.on_click = Func(player.animate_position, (hookshot_target.x, hookshot_target.y-2,hookshot_target.z), duration=.5, curve=curve.linear)


app.run()