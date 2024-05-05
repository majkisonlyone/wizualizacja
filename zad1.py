import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from renderer import Renderer

def polygon():
    glBegin(GL_POLYGON) #GL_LINE_LOOP

    radius = side_length / (2 * math.sin(math.pi / sides))
    for i in range(sides):
        angle = 2 * math.pi * i / sides
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glVertex2f(x, y)
    
    glEnd()

sides = int(input("Podaj ilość boków N: "))
side_length = float(input("Podaj długość boku d: ")) / 10

renderer = Renderer("zadanie1.py")
renderer.render_with_shader(polygon)
