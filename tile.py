from PIL import Image
import random

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
