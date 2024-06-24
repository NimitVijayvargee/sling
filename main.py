from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
from ursina.prefabs.sky import Sky
from ursina.shaders import basic_lighting_shader
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
for x in os.listdir("assets/textures/pooltile_temps"):
            try:
                os.remove(f"assets/textures/pooltile_temps/{x}")
            except:
                print(f'failed to remove file {x}')
                
scene.fog_density = (50, 200)
scene.fog_color = rgb(3, 87, 76)
reloading = False

tile.genPlane((0,-4,0),(0,0,0))
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
        for x in os.listdir("assets/textures/pooltile_temps"):
            try:
                os.remove(f"assets/textures/pooltile_temps/{x}")
            except:
                print(f'failed to remove file {x}')
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

player = FirstPersonController()
player.position = Vec3(0, 50, 0)
gun.has_gun = False
player.hp = 100
info = Text(text=f"HP: {player.hp}/100 \nAmmo: {gun.ammo}/{gun.max_reload}", position=window.top_left)
gun.on_click = gun.get_gun
print(player.scale)
app.run()
