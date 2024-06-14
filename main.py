from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
from ursina.prefabs.sky import Sky
from ursina.prefabs.trail_renderer import TrailRenderer
ammo = 0
app = Ursina(borderless=False,title='Sling')
window.exit_button.visible = False

sky = Sky()
map = Entity(model='/assets/maps/map1.obj',texture='/assets/textures/tile.png', scale=.5, position=(-10,0,-10),rotate=Vec3(0,90,0), collider='mesh')
reloading = False

active_bullets = []
def shoot():
    if not reloading:
        global ammo, active_bullets
        ammo -= 1
        gun.rotation = (0,0,0)
        bullet = Entity(parent=gun, model='cube', scale=(.05,.05,.25), color=color.yellow, position=(-0.3,1.5,0.3), collider='box')
        bullet.world_parent = scene
        active_bullets.append(bullet)
        invoke(setattr,bullet,"color",color.black, delay=0.2)
        hitinfo = raycast(bullet.position, bullet.rotation,distance=250, ignore=(active_bullets))
        if hitinfo.hit:
            distance = hitinfo.distance
            bullet.animate_position(bullet.position+(bullet.forward*distance*0.25), curve=curve.linear, duration=4)
        else:
            bullet.animate_position(bullet.position+(bullet.forward*1000), curve=curve.linear, duration=4)
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
            invoke(reload,delay=2.5)

    if mouse.left and player.gun: 
        if ammo < 1:
            return None
        else:
            shoot()
            Wait(1)
        

def reload():
    global ammo, reloading
    ammo = 40
    reloading = False

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
player.position = Vec3(0,50,0)
player.gun = None
player.hp = 100
info = Text(text=f"HP: {player.hp}/100 \nAmmo:{ammo}/40")
gun.on_click = get_gun
    

hookshot_target = Button(parent=scene, model='cube', color=color.brown, position=(4,5,5))
hookshot_target.on_click = Func(player.animate_position, (hookshot_target.x, hookshot_target.y-2,hookshot_target.z), duration=.5, curve=curve.linear)


app.run()