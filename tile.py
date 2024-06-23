from PIL import Image
import random
from ursina import *

#this works; don't touch it
def repeat_texture(texture_path, x_len, z_len):
    texture = Image.open(texture_path)
    texture_width, texture_height = texture.size
    new_width = texture_width * x_len
    new_height = texture_height * z_len
    new_image = Image.new('RGB', (new_width, new_height))
    for i in range(x_len):
        for j in range(z_len):
            rotated_texture = texture.rotate(random.choice([0, 90, 180, 270]))
            new_image.paste(rotated_texture, (i * texture_width, j * texture_height))
    
    new_image.save(f"assets/textures/pooltile_temps/pooltile_{x_len}x{z_len}.png")

def genPlane(offset,rotate=(0,0,0)):
    x_offset, y_offset, z_offset = offset
    x_len, z_len = random.randint(10,30),random.randint(10,30)
    repeat_texture('assets/textures/pooltile.png',x_len,z_len)
    Entity(texture = f"/assets/textures/pooltile_temps/pooltile_{x_len}x{z_len}.png",
            model = 'plane',
            collider = 'box',
            scale = (2*x_len,2,2*z_len),
            position=((x_len / -2)+x_offset,  y_offset,  (z_len / -2)+z_offset),
            rotation = (rotate)
            )
    
def genRoom(offset,size):
    x,y,z= size
    genPlane(offset,(0,))