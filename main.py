from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
from ursina.prefabs.sky import Sky
from gun import Gun

app = Ursina(borderless=False,title='Sling')
window.exit_button.visible = False


sky = Sky()
map = Entity(model="cube",texture="assets/textures/tile.png", scale=(25,1,25), position=(0,-20,0), collider='mesh')
reloading = False

active_bullets = []

def update():
    global reloading
    info.text = f"HP: {player.hp}/100 \nAmmo:{gun.ammo}/40"
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
        if gun.has_gun and not gun.reloading:
            gun.reloading=True
            Audio(sound_file_name=gun.reload_sound)
            invoke(gun.reload,delay=2.5)

    if mouse.left and gun.has_gun: 
        if gun.ammo < 1:
            return None
        else:
            gun.shoot()
            Wait(1)
        



gun = Gun(parent=scene, model='/assets/models/gun/ump45', origin_y=-.5, position=(3,0,3), collider='box', color=color.black)


player = FirstPersonController()
player.position = Vec3(0,50,0)
gun.has_gun = None
player.hp = 100
info = Text(text=f"HP: {player.hp}/100 \nAmmo:{gun.ammo}/40")
gun.on_click = gun.get_gun
    

hookshot_target = Button(parent=scene, model='cube', color=color.brown, position=(4,5,5))
hookshot_target.on_click = Func(player.animate_position, (hookshot_target.x, hookshot_target.y-2,hookshot_target.z), duration=.5, curve=curve.linear)


app.run()