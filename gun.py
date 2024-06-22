from ursina import *

class Gun(Button):
    reload_sound = "assets/soundfiles/reload.mp3"   # reload sound
    pew = "assets/soundfiles/shotgun_pew.mp3"               # pew pew sound
    bullets = 7                                     # bullet count per shot        
    delay = 2                                       # delay shooting; seconds
    spread = 10                                     # bullet spread; degrees
    damage = 10                                     # gun.damage like no shit
    maxdist = 20                                    # max distance after which damage becomes 0 (damage reduces linearly,
                                                    # set to extremely large amount when working
                                                    # with snipers or long distance ARs)
    recoil = 10                                     #player recoil
    max_reload = 5                                  # maximum gun reload
    reloading = False                               # is gun reloading right now?
    ammo = 0                                        # gun ammo (set to max reload when reloading or when gun picked up)
    can_shoot = True                                # is gun shooting right now?
    active_bullets = []                             # Active bullets (for collisions)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def shoot(self):
        if self.can_shoot and not self.reloading:
            self.can_shoot = False
            invoke(self.allow_shooting, delay=self.delay)

            # Initialize bullet
            self.ammo -= 1
            self.rotation = (0, -7, 0)
            pewsound = Audio(sound_file_name=self.pew)
            for _ in range(self.bullets):
                bullet = Entity(
                    parent=self,
                    model='cube',
                    scale=(.05, .05, .25),
                    color=color.yellow,
                    position=(-0.3, 1.5, 0.3),
                    collider='box',
                    world_parent=scene
                )

                self.active_bullets.append(bullet)
                # Bullet motion
                invoke(setattr, bullet, "color", color.black, delay=0.2)  # colour effect
                bullet.rotation_x += random.randint(round(self.spread / -2), round(self.spread / 2))  # Bullet spread
                bullet.rotation_y += random.randint(round(self.spread / -2), round(self.spread / 2))
                bullet.rotation_z += random.randint(round(self.spread / -2), round(self.spread / 2))
                bullet.animate_position(bullet.position + (bullet.forward * 1000), curve=curve.linear, duration=4)  # forward

                destroy(bullet, delay=3)
            
            # Reset gun and destroy bullet
            player = self.parent.parent #grandparent of the gun is the player
            player.animate_rotation((player.rotation_x - self.recoil, player.rotation_y, player.rotation_z), duration=0.2)
            player.animate_rotation((player.rotation_x + (self.recoil-10), player.rotation_y, player.rotation_z), duration=1, delay=0.25)
            self.rotation = (0, 270, 0)
            
    def allow_shooting(self):
        self.can_shoot = True

    def get_gun(self):
        self.parent = camera
        self.position = Vec3(.5, -.6, .5)
        self.scale = (0.3, 0.3, 0.3)
        self.rotation = (0, 270, 0)
        self.ammo = self.max_reload
        self.has_gun = True

    def reload(self):
        self.ammo = self.max_reload
        self.reloading = False