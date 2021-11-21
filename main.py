from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


app = Ursina()

window.fps_counter.enabled = False
window.exit_button.visible = False

blocks = [
    load_texture('assets/grass.png'),
    load_texture('assets/grass.png'),
    load_texture('assets/stone.png'),
    load_texture('assets/gold.png'),
    load_texture('assets/lava.png'),
]

block_id = 1

def input(key):
    global block_id
    if key.isdigit():
        block_id = int(key)
        if block_id >= len(blocks):
            block_id = len(blocks) - 1
        

sky = Entity(
    parent=scene,
    model="sphere",
    texture=load_texture("assets/sky.jpg"),
    scale=500,
    double_sided=True
)

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture="assets/grass.png"):
        super().__init__(
            parent=scene,
            position=position,
            origin_y=0.5,
            model="assets/block",
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            scale=1.0
        )
    
    def input(self, key):
        if self.hovered:
            if key== "left mouse down":
                Voxel(position=self.position + mouse.normal, texture=blocks[block_id])
            elif key == "right mouse down":
                destroy(self)
        
for z in range(20):
    for x in range(20):
        voxel = Voxel(position=(x, 0,z))

player = FirstPersonController()
        
app.run()   