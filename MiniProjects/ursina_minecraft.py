from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

player = FirstPersonController()
Sky()

boxes = []
MAX_REACH = 5


def add_box(position):
    block = Entity(
        parent=scene,
        model='cube',
        texture='grass',
        color=color.white,     # force full texture color
        position=position,
        scale=1,
        collider='box'
    )
    boxes.append(block)


# flat world
for x in range(20):
    for z in range(20):
        add_box((x, 0, z))


# selection highlight
highlight = Entity(
    parent=scene,
    model='cube',
    color=color.white,
    scale=1.01,
    visible=False,
    wireframe=True
)


def update():
    hovered = mouse.hovered_entity
    if hovered in boxes:
        highlight.position = hovered.position
        highlight.visible = True
    else:
        highlight.visible = False


def input(key):
    hovered = mouse.hovered_entity
    if hovered in boxes and distance(player.position, hovered.position) <= MAX_REACH:
        if key == 'left mouse down':
            add_box(hovered.position + mouse.normal)
        if key == 'right mouse down':
            boxes.remove(hovered)
            destroy(hovered)

app.run()