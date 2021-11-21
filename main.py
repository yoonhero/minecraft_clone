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

# store current map size [smallestX, largestX, smallestZ, largestZ]
map = [0, 0, 0, 0]

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

player = FirstPersonController()

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
    
    def update(self):
        # if player further from block
        if self.x < player.x - 10:
            if self.z < player.z - 10:
                destroy(self)


def randomSpawn(freq):
    if math.ceil(math.random() * freq) == math.ceil(freq / 2):
        return True
    return False

noise = PerlinNoise(octaves=3, seed=2021)
shells = []

def updateMap(x, z, amp=0):
    global map
    if map[2] >= z + amp:
        map[2] = z
    elif map[3] <= z - amp:
        map[3] = z
    if map[0] >= x + amp:
        map[0] = x
    elif map[1] <= x - amp:
        map[1] = x

# make 20*20 block
for z in range(20):

    for x in range(20):
        updateMap(x, z, 0)
        # random height
        height = .25 + noise([x/24, z/24])
        height = math.floor(height * 7)
        
        # randomly landscape 
        if height >= 0:
            for y in range(height+1):
                voxel = Voxel(position=(x, y, z))
                if y == height:
                    shells.append(voxel)
                    
                    # original = shells[x]
                    # if original == None:
                    #     newDict = {y:voxel}
                    #     shells[x] = newDict
        else:
            # water 
            voxel = Voxel(position=(x, 0, z))


amp = 4

# infinite terrian
def generateMoreBlock(amp):
    shellWidth = 20
    freq = 24
    for i in range(len(shells)):
    	shells[i].x = floor((i/shellWidth) + player.x - 0.5*shellWidth)
		shells[i].z = floor((i%shellWidth) + player.z - 0.5*shellWidth)
		shells[i].y = floor(noise([x/freq, z/freq])*amp)


def update():
    global map
    if held_keys["left mouse"] or held_keys["right mouse"]:
        punch.play()
        hand.position = Vec2(0.4, -0.5)
    else:
        hand.position = Vec2(0.6, -0.6)

    current_position = [player.x, player.z]
    
    if current_position[0] < map[0] + amp:
        map[0] = math.ceil(current_position[0]) - amp
        # create more block
        generateMoreBlock(amp)
        
    elif current_position[0] > map[1] - amp:
        map[1] = math.ceil(current_position[0]) + amp
        # craete more blocks
        generateMoreBlock(amp)
        
    if current_position[1] < map[2] + amp:
        map[2] = math.ceil(current_position[1]) - amp
        # create more block
        generateMoreBlock( amp)
        
    elif current_position[1] > map[3] - amp:
        map[3] = math.ceil(current_position[1]) + amp
        # craete more blocks
        generateMoreBlock(amp)
    
    

        
    
        
app.run()   