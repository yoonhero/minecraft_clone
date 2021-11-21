from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import math
from perlin_noise import PerlinNoise

app = Ursina()

window.fps_counter.enabled = False
window.exit_button.visible = False

punch = Audio('assets/punch', autoplay=False)

blocks = [
    load_texture('assets/grass.png'),
    load_texture('assets/grass.png'),
    load_texture('assets/stone.png'),
    load_texture('assets/gold.png'),
    load_texture('assets/lava.png'),
]

block_id = 1

def input(key):
    global block_id, hand
    if key.isdigit():
        block_id = int(key)
        if block_id >= len(blocks):
            block_id = len(blocks) - 1
        
        hand.texture = blocks[block_id]

sky = Entity(
    parent=scene,
    model="sphere",
    texture=load_texture("assets/sky.jpg"),
    scale=500,
    double_sided=True
)

hand = Entity(
    parent=camera.ui,
    model='assets/block',
    texture=blocks[block_id],
    scale=0.2,
    rotation=Vec3(-10, -10, 10), 
    position=Vec2(0.6, -0.6)
)

def update():
    if held_keys["left mouse"] or held_keys["right mouse"]:
        punch.play()
        hand.position = Vec2(0.4, -0.5)
    else:
        hand.position = Vec2(0.6, -0.6)


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture="assets/grass.png"):
        super().__init__(
            parent=scene,
            position=position,
            model="assets/block",
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            scale=0.5
        )
    
    def input(self, key):
        if self.hovered:
            if key== "left mouse down":
                Voxel(position=self.position + mouse.normal, texture=blocks[block_id])
            elif key == "right mouse down":
                destroy(self)
                
noise = PerlinNoise(octaves=3, seed=1002000)

for z in range(20):
    for x in range(20):
        # random height
        height = .25 + noise([x/20, z/20])
        
        # randomly landscape 
        voxel = Voxel(position=(x, height, z))

player = FirstPersonController()
        
app.run()   