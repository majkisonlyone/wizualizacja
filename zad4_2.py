from renderer import Renderer
from figures import Cube, Pyramid, Cone, Cylinder

renderer = Renderer("zadanie2.py")

objects_to_render = [
    Cube(-0.2, 0.5, 0, (1, 1, 0, 1), [45, 45, 45]).display(),
    Pyramid(0.5, -0.5, 0, (1, 1, 0, 1), [45, 30, 0]).display(),
    Cone(-0.7, 0.5, 0, (1, 1, 0, 1), [2 * 3.14 / 3, 0, 0]).display(),
    Cylinder(-0.7, -0.5, 0, (1, 1, 0, 1), [2 * 3.14 / 3, 0, 0]).display(),
]
renderer.render_with_shader(objects_to_render)
