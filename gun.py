from ursina import *

class Gun(Button):
    reload_sound = "assets/soundfiles/reload.mp3"
    shoot = "assets/soundfiles/pew.mp3"
    bullets = 1
    delay = 0
    spread = 0
    max_reload = 40
    reloading = False
    ammo = 0
    active_bullets = []
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def shoot(self):
        if not self.reloading:
            self.ammo -= 1
            self.rotation = (0,0,0)
            bullet = Entity(parent=self, model='cube', scale=(.05,.05,.25), color=color.yellow, position=(-0.3,1.5,0.3), collider='box')
            bullet.world_parent = scene
            self.active_bullets.append(bullet)
            invoke(setattr,bullet,"color",color.black, delay=0.2)
            hitinfo = raycast(bullet.position, bullet.rotation,distance=250, ignore=tuple(self.active_bullets))
            if hitinfo.hit:
                distance = hitinfo.distance
                bullet.animate_position(bullet.position+(bullet.forward*distance*0.25), curve=curve.linear, duration=4)
            else:
                bullet.animate_position(bullet.position+(bullet.forward*1000), curve=curve.linear, duration=4)
            self.rotation = (0,270,0)
            destroy(bullet, delay=3)

    def get_gun(self):
        self.parent = camera
        self.position = Vec3(.5,-.6,.5)
        self.scale = (0.3,0.3,0.3)
        self.rotation = (0,270,0)
        self.ammo = 40
        self.has_gun = True
    
    def reload(self):
        self.ammo = self.max_reload
        self.reloading = False