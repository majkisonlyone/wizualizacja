from time import sleep
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import numpy as np
from renderer import Renderer
from figures import Sphere

stop_rotating = False

x_angle = 0
y_angle = 0
z_angle = 0

def rotating_objects():
    global x_angle
    global y_angle
    global z_angle
    return [
       Sphere(0.5, 0.5, 0.5, (1, 0, 0, 1), [x_angle, y_angle, z_angle]).set_dimensions(0.3,3).display(),
       Sphere(-1, 1, 0.7, (1, 0, 0, 1), [x_angle, y_angle, z_angle]).set_dimensions(0.4,3).display(),
       Sphere(-0.2, -0.2, 0.2, (1, 0, 0, 1), [x_angle, y_angle, z_angle]).set_dimensions(0.5,3).display(),
    ]
#todo: parametry projekcji, ruch kamery
def spin():
    global x_angle
    global y_angle
    global z_angle
    # if not stop_rotating:
    #     x_angle += 0.05
    #     y_angle += 0.05
    #     z_angle += 0.05
    sleep(0.1)
    glutPostRedisplay()

def keyboard_interrupt(k, x, y):
    global stop_rotating
    stop_rotating = not stop_rotating

renderer = Renderer("zadanie3.py")
renderer.render_with_shader_rot_cam("pers",rotating_objects, spin, keyboard_interrupt)