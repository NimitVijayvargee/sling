from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
from ursina.prefabs.sky import Sky
from gun import Gun
from enemy import Enemy
import time

app = Ursina(borderless=False, title='Sling')
window.exit_button.visible = False

sky = Sky()
map = Entity(model="cube", texture="assets/textures/tile.png", scale=(25, 1, 25), position=(0, -1, 0), collider='mesh')
enemy = Enemy(model="assets/models/person", collider="box",rotation=(270,0,90), scale=0.3, color=color.blue)

reloading = False

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

player = FirstPersonController()
player.position = Vec3(0, 50, 0)
gun.has_gun = False
player.hp = 100
info = Text(text=f"HP: {player.hp}/100 \nAmmo: {gun.ammo}/{gun.max_reload}", position=window.top_left)
gun.on_click = gun.get_gun
hookshot_target = Button(parent=scene, model='cube', color=color.brown, position=(4, 5, 5))
hookshot_target.on_click = Func(player.animate_position, (hookshot_target.x, hookshot_target.y - 2, hookshot_target.z), duration=.5, curve=curve.linear)
 
app.run()

