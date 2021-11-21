from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


app = Ursina()

window.fps_counter.enabled = False
window.exit_button.visible = False

Entity(
    parent=scene,
    model="sphere",
    texture=load_texture("assets/sky.jpg"),
    scale=500,
    double_sided=True
)

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture="brick"):
        super().__init__(
            parent=scene,
            position=position,
            origin_y=0.5,
            model="cube",
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            scale=1.0
        )
        
for z in range(20):
    for x in range(20):
        voxel = Voxel(position=(x, 0,z))

player = FirstPersonController()
        
app.run()   