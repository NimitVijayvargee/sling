from ursina import *

class Enemy(Entity):
    hp = 100


    def killed(self):
        self.animate_position((0,-50,0),5)
        destroy(self)