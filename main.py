from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
from ursina.prefabs.sky import Sky
from gun import Gun

ammo = 0
app = Ursina(borderless=False,title='Sling')
window.exit_button.visible = False


sky = Sky()
map = Entity(model="cube",texture="assets/textures/tile.png", scale=(25,1,25), position=(0,-20,0), collider='mesh')
reloading = False

active_bullets = []

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
            reloading=True
            invoke(reload,delay=2.5)

    if mouse.left and player.gun: 
        if ammo < 1:
            return None
        else:
            shoot()
            Wait(1)
        



gun = Gun()
def get_gun(self):
    entity = self.entity
    entity.parent = camera
    entity.position = Vec3(.5,-.6,.5)
    entity.scale = (0.3,0.3,0.3)
    entity.rotation = (0,270,0)
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