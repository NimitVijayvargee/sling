from ursina import *

class Gun():
    #settings for UMP45
    model = "assets/models/gun/ump45"
    reload = "assets/soundfiles/reload.mp3"
    shoot = "assets/soundfiles/pew.mp3"
    bullets = 1
    delay = 0
    spread = 0
    max_reload = 4
    entity = Entity(parent=scene, model=model,  origin_y=-.5, position=(3,0,3), collider='box', color=color.black)
    
    def shoot():
        if not reloading:
            global active_bullets, player, ammo
            ammo -= 1
            gun.rotation = (0,0,0)
            Audio(sound_file_name=shoot)
            bullet = Entity(parent=gun, model='cube', scale=(.05,.05,.25), color=color.yellow, position=(-0.3,1.5,0.3),rotatation=(random.randrange(spread),random.randrange(spread),random.randrange(spread)),collider='box')
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

    def reload(self):
        global ammo, reloading
        Audio(sound_file_name='/assets/soundfiles/reload.mp3')
        ammo = self.max_reload
        reloading = False

    def get_gun():
        global player, ammo
        entity.parent = camera
        entity.position = Vec3(.5,-.6,.5)
        entity.scale = (0.3,0.3,0.3)
        entity.rotation = (0,270,0)
        player.gun = 'ump45'
        ammo = gun.max_reload

    
