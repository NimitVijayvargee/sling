import random
from PIL import Image, ImageDraw
import numpy as np
from ursina import *

def random_colour(r_limit, g_limit, b_limit):
    rl, ru = r_limit
    gl, gu = g_limit
    bl, bu = b_limit
    r = random.randint(rl, ru)
    g = random.randint(gl, gu)
    b = random.randint(bl, bu)
    return f"#{r:02x}{g:02x}{b:02x}"

def repeat_texture(texture_path, x_len, z_len):
    try:
        texture = Image.open(f"assets/textures/pooltile_temps/pooltile_{x_len}x{z_len}.png")
        return texture
    except:
        texture = Image.open(texture_path)
        texture_width, texture_height = texture.size
        new_width = texture_width * x_len
        new_height = texture_height * z_len
        new_image = Image.new('RGB', (new_width, new_height))

        recoulered_texture = ImageDraw.Draw(texture)
        for i in range(x_len):
            for j in range(z_len):
                colour = random_colour((0, 20), (100, 255), (180, 255))
                recoulered_texture.rectangle([(1, 1), (14, 14)], fill=colour)
                new_image.paste(texture, (i * texture_width, j * texture_height))

        new_image.save(f"assets/textures/pooltile_temps/pooltile_{x_len}x{z_len}.png")

def genPlane(offset, rotate=(0, 0, 0), x_len=None, z_len=None):
    x_offset, y_offset, z_offset = offset
    if x_len is None:
        x_len = random.randint(50, 150)
    if z_len is None:
        z_len = random.randint(50, 150)
    
    repeat_texture('assets/textures/pooltile.png', x_len, z_len)
    Entity(
        texture=f"assets/textures/pooltile_temps/pooltile_{x_len}x{z_len}.png",
        model='plane',
        collider='box',
        scale=(0.3 * x_len, 2, 0.3 * z_len),
        position=((x_len / -8) + x_offset, y_offset, (z_len / -8) + z_offset),
        rotation=rotate
    )

def genRoom(offset, size):
    x, y, z = size
    xo,yo,zo = offset
    print(x,y,z,"\n",xo,yo,zo)
    genPlane(offset, (0,0,0), x*7,z*7)       #floor
    genPlane((xo,yo+y,zo), (0,0,180), x*8,z*8)     #ceiling
    genPlane((xo,yo,zo-z), (90,0,0), x*8,y*8)
    genPlane((xo,yo,zo+z), (270,0,0), x*8,y*8)
    genPlane((xo-x,yo,zo), (0,0,90), x*8,y*8)
    genPlane((xo+x,yo,zo), (0,0,270), x*8,y*8)
