from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
from ursina.prefabs.sky import Sky
from ursina.shaders import colored_lights_shader as lit
from os import remove as delete
from os import makedirs as createfolder
#my external code stuffs
from gun import Gun
from enemy import Enemy
import tile

app = Ursina(borderless=False, title='PoolLoop')
window.exit_button.visible = False
sky = Sky()
enemy = Enemy(model="assets/models/person", collider="box",rotation=(270,0,90), scale=0.3, color=color.blue)

reloading = False

def genMap():
    x_len, z_len = random.randint(10,30),random.randint(10,30)
    tile.repeat_texture('assets/textures/pooltile.png',x_len,z_len)
    Entity(texture = f"/assets/textures/pooltile_temps/pooltile_{x_len}x{z_len}.png",
            model = 'plane',
            collider = 'box',
            scale = (2*x_len,2,2*z_len),
            position=((x_len / -2),-4,(z_len / -2))
            )

genMap()
def update():
    global reloading,enemy
    info.text = f"HP: {player.hp}/100 \nAmmo: {gun.ammo}/{gun.max_reload}"
    if held_keys['-'] and player.hp != 0:
        player.hp -= 1
    if held_keys['='] and player.hp != 100:
        player.hp += 1
    if player.hp == 0:
        info.text = "rip bozo you dead"
        time.sleep(3)
        quit()
    if held_keys['escape']:
        quit()
    if held_keys['r']:
        if gun.has_gun and not gun.reloading and gun.ammo < gun.max_reload:
            gun.reloading = True
            Audio(sound_file_name=gun.reload_sound)
            invoke(gun.reload, delay=2.5)

    if mouse.left and gun.has_gun: 
        if gun.ammo < 1:
            return
        else:
            gun.shoot()
    for bullet in gun.active_bullets:
        if enemy:
            if bullet.intersects(enemy):
                print("Hit!")
                destroy(bullet)
                enemy.blink(color.red, 0.1)
                enemy_distance = distance(player,enemy)
                distance_multiplier = gun.maxdist - enemy_distance
                if distance_multiplier < 0:
                    distance_multiplier = 0
                enemy.hp -= gun.damage * distance_multiplier
                break

    if enemy:
        enemy.look_at_xz(player)
    if enemy.hp < 1:
        enemy.color = color.red
        destroy(enemy,delay=1)


gun = Gun(parent=scene, model='assets/models/gun/ump45', origin_y=-.5, position=(3, 0, 3), collider='box', color=color.black)

player = FirstPersonController(shader=lit)
player.position = Vec3(0, 50, 0)
gun.has_gun = False
player.hp = 100
info = Text(text=f"HP: {player.hp}/100 \nAmmo: {gun.ammo}/{gun.max_reload}", position=window.top_left)
gun.on_click = gun.get_gun

app.run()
