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
    def __init__(self, position=(0, 0, 0), texture="assets/grass.png", tree=False):
        self.tree = tree
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
                shells.pop()
    
    def update(self):
        # if player further from tree block
        if self.tree:
            if self.x < player.x - 7 or self.x > player.x+7:
                if self.z < player.z - 7 or self.z > player.z+7:
                    destroy(self)

# craete Tree
class Tree(Button):
    def __init__(self, position=[0, 0, 0], treeHeight=6):
        self.position = [position[0], position[2]]
        for h in range(0, treeHeight-2):
            height = position[1]
            Voxel(position=(position[0], height + h, position[2]), texture=blocks[2], tree=True)
        
        for y in range(0, 2):
            height = position[1] + treeHeight - 2
            for x in range(0,2-y):
                for z in range(0,2-y):
                    Voxel(position=(position[0]+x, height+y, position[2]+z), tree=True)
                    Voxel(position=(position[0]-x, height+y, position[2]-z), tree=True)
                    Voxel(position=(position[0]-x, height+y, position[2]+z), tree=True)
                    Voxel(position=(position[0]+x, height+y, position[2]-z), tree=True)
    def update(self):
        # if player further from tree
        if self.position[0] < player.x - 10:
            if self.position[1] < player.z - 10:
                destroy(self)

def randomSpawn(freq):
    if math.ceil(random.random() * freq) == math.ceil(freq / 2):
        return True
    return False

noise = PerlinNoise(octaves=3, seed=random.randrange(1, 10000000000000000000000000000))

shells = []

amp = 6
freq = 24                                                                                                                          
shellWidth = 20

# make 20*20 block
for z in range(shellWidth):

    for x in range(shellWidth):
        # random height
        height = .25 + noise([x/freq, z/freq])
        height = math.floor(height * amp)
        
        # randomly landscape 
        if height >= 0:
            voxel = Voxel(position=(x, height, z))
            shells.append(voxel)
            # for y in range(height+1):
            #     voxel = Voxel(position=(x, y, z))
            #     if y == height:
            #         shells.append(voxel)
                # instantShells.append(voxel)
                    
                    # original = shells[x]
                    # if original == None:
                    #     newDict = {y:voxel}
                    #     shells[x] = newDict
        else:
            # water 
            voxel = Voxel(position=(x, 0, z))
            shells.append(voxel)
        
        # shells.append(instantShells)

treeFreq = 100

# infinite terrian
def generateMoreBlock():
    global amp, freq, shellWidth
    if len(shells) == shellWidth**2:
        for i in range(len(shells)):
            try: 
                shell = shells[i]
                shell.x = floor((i/shellWidth) + player.x - 0.5*shellWidth)
                shell.z = floor((i%shellWidth) + player.z - 0.5*shellWidth)
                shell.y = floor(noise([shell.x/freq, shell.z/freq])*amp)
            except:
                continue
    else:
        while len(shells) != shellWidth**2:
            voxel = Voxel(position=(0, 0, 0)) 
            shells.append(voxel)
        
        
        
# create Tree        
Tree(position=[3,0,4])

def update():
    # when player falling
    if player.y < -30:
    		player.y = 10
      
    if held_keys["left mouse"] or held_keys["right mouse"]:
        punch.play()
        hand.position = Vec2(0.4, -0.5)
    else:
        hand.position = Vec2(0.6, -0.6)

    generateMoreBlock()
    
    # if randomSpawn(treeFreq):
    #         Tree(position=[shell.x, shell.y, shell.z])

        
    
        
app.run()   