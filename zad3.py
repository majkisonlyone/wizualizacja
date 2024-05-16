from time import sleep
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import numpy as np
from renderer import Renderer
from figures import Cube, Pyramid, Cone, Cylinder

stop_rotating = False

x_angle = 0
y_angle = 0
z_angle = 0

objects_to_render = [
    Cube(-0.2, 0.5, 0, (1, 1, 0), [x_angle, y_angle, z_angle]).display(),
    Pyramid(0.5, -0.5, 0, (1, 1, 0), [x_angle, y_angle, z_angle]).display(),
    Cone(-0.7, 0.5, 0, (1, 1, 0), [x_angle, y_angle, z_angle]).display(),
    Cylinder(-0.7, -0.5, 0, (1, 1, 0), [x_angle, y_angle, z_angle]).display(),
]

# def rotating_objects():
#     rotating_cube(x_angle, y_angle, z_angle)
#     rotating_pyramid(d_pyramid, h_pyramid, x_angle, y_angle, z_angle)
#     rotating_cylinder(r_cylinder, h_cylinder, x_angle, y_angle, z_angle)
#     rotating_cone(r_cone, h_cone, x_angle, y_angle, z_angle)

def rotating_objects():
    global x_angle
    global y_angle
    global z_angle
    print("xangle" + str(x_angle))
    return [
        Cube(-0.2, 0.5, 0, (1, 1, 0), [x_angle, y_angle, z_angle]).display(),
        Pyramid(0.5, -0.5, 0, (1, 1, 0), [x_angle, y_angle, z_angle]).display(),
        Cone(-0.7, 0.5, 0, (1, 1, 0), [x_angle, y_angle, z_angle]).display(),
        Cylinder(-0.7, -0.5, 0, (1, 1, 0), [x_angle, y_angle, z_angle]).display(),
    ]

def spin():
    global x_angle
    global y_angle
    global z_angle
    # global objects_to_render
    if not stop_rotating:
        x_angle += 0.05
        y_angle += 0.05
        z_angle += 0.05
        # print("rotae")
#     objects_to_render = [
#         Cube(-0.2, 0.5, 0, (1, 1, 0), [x_angle, y_angle, z_angle]).display(),
#         Pyramid(0.5, -0.5, 0, (1, 1, 0), [x_angle, y_angle, z_angle]).display(),
#         Cone(-0.7, 0.5, 0, (1, 1, 0), [x_angle, y_angle, z_angle]).display(),
#         Cylinder(-0.7, -0.5, 0, (1, 1, 0), [x_angle, y_angle, z_angle]).display(),
# ]
    sleep(0.1)
    glutPostRedisplay()

def keyboard_interrupt(k, x, y):
    global stop_rotating
    stop_rotating = not stop_rotating


# display = (800, 600)

# Prostopadłościan
# a = float(input("a: "))
# b = float(input("b: "))
# c = float(input("c: "))

# # Ostroslup
# d_pyramid = float(input("d (ostroslup): "))
# h_pyramid = float(input("h (ostroslup): "))

# # Cylinder
# r_cylinder = float(input("r (cylinder): "))
# h_cylinder = float(input("h (cylinder): "))

# # Stożek
# r_cone = float(input("r (stozek): "))
# h_cone = float(input("h (stozek): "))


renderer = Renderer("zadanie3.py")
renderer.render_with_shader_rot(rotating_objects, spin, keyboard_interrupt)
