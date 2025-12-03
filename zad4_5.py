from time import sleep
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import numpy as np
from renderer import Renderer
from figures import Cube, Pyramid, Cone, Cylinder, Sphere

stop_rotating = False

r = float(input("Podaj r (sugestia od 0.1 do 0.5): "))  # 0.4
q = int(input("Podaj q (sugestia od 1 do 5): "))  # 2

x_angle = 0
y_angle = 0
z_angle = 0


def rotating_objects():
    global x_angle
    global y_angle
    global z_angle
    return [
        Sphere(-0.2, 0.5, 0.5, (1, 0, 0, 1), [x_angle, y_angle, z_angle])
        .set_dimensions(r, q)
        .display(),
    ]


def spin():
    global x_angle
    global y_angle
    global z_angle
    if not stop_rotating:
        x_angle += 0.05
        y_angle += 0.05
        z_angle += 0.05
    sleep(0.1)
    glutPostRedisplay()


def keyboard(k, x, y):
    global dist, angl_left_right
    if k == b"w":
        dist -= 0.1
    if k == b"s":
        dist += 0.1
    if k == b"a":
        angl_left_right += 0.1
    if k == b"d":
        angl_left_right -= 0.1
    if k == b"q":
        glutLeaveMainLoop()


renderer = Renderer("zadanie4_5.py")
renderer.render_with_shader_rot_cam("orth", rotating_objects, spin, keyboard)
