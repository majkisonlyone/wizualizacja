from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from renderer import Renderer


def cube():
    a_new = a / 2
    b_new = b / 2
    c_new = c / 2
    vertices = (
        (a_new, -c_new, -b_new),
        (a_new, c_new, -b_new),
        (-a_new, c_new, -b_new),
        (-a_new, -c_new, -b_new),
        (a_new, -c_new, b_new),
        (a_new, c_new, b_new),
        (-a_new, -c_new, b_new),
        (-a_new, c_new, b_new),
    )

    edges = (
        (0, 1),
        (0, 3),
        (0, 4),
        (2, 1),
        (2, 3),
        (2, 7),
        (6, 3),
        (6, 4),
        (6, 7),
        (5, 1),
        (5, 4),
        (5, 7),
    )

    glPushMatrix()
    gluPerspective(45, (display[0] / display[1]), 0.1, 70.0)
    glTranslatef(-15, 0.0, -50)
    glRotatef(75, 0, 1, 1)

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    glPopMatrix()


def pyramid():
    d_new = h_pyramid / 2
    triangle_h = math.sqrt(3) / 2 * d_pyramid
    vertices = (
        (0.0, triangle_h, 0.0),  # Apex
        (d_new, 0.0, -d_new),
        (-d_new, 0.0, d_new),
        (0.0, 0.0, d_new * math.sqrt(3)),
    )

    edges = ((0, 1), (0, 2), (0, 3), (1, 2), (2, 3), (3, 1))

    glPushMatrix()
    gluPerspective(45, (display[0] / display[1]), 0.1, 70.0)
    glTranslatef(-5, 0.0, -50)
    glRotatef(10, 1, 0, 0)

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    glPopMatrix()


def cylinder():
    num_segments = 100
    vertices = []
    edges = []

    for i in range(num_segments):
        angle = 2 * math.pi * i / num_segments
        x = r_cylinder * math.cos(angle)
        y = r_cylinder * math.sin(angle)
        vertices.append((x, y, -h_cylinder / 2))

    for i in range(num_segments):
        angle = 2 * math.pi * i / num_segments
        x = r_cylinder * math.cos(angle)
        y = r_cylinder * math.sin(angle)
        vertices.append((x, y, h_cylinder / 2))

    for i in range(num_segments):
        edges.append((i, (i + 1) % num_segments))
        edges.append((i + num_segments, (i + 1) % num_segments + num_segments))
        edges.append((i, i + num_segments))

    glPushMatrix()
    gluPerspective(45, (display[0] / display[1]), 0.1, 70.0)
    glTranslatef(5, 0.0, -50)
    glRotatef(75, 0, 1, 1)

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    glPopMatrix()


def cone():
    num_segments = 100
    vertices = []
    edges = []

    for i in range(num_segments):
        angle = 2 * math.pi * i / num_segments
        x = r_cone * math.cos(angle)
        y = r_cone * math.sin(angle)
        vertices.append((x, y, -h_cone / 2))

    vertices.append((0, 0, h_cone / 2))

    for i in range(num_segments):
        edges.append((i, (i + 1) % num_segments))

    for i in range(num_segments):
        edges.append((i, num_segments))

    glPushMatrix()
    gluPerspective(45, (display[0] / display[1]), 0.1, 70.0)
    glTranslatef(15, 0, -50)
    glRotatef(45, 0, 1, 1)

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    glPopMatrix()


def objects():
    cylinder()
    cube()
    pyramid()
    cone()


display = (800, 600)

# Prostopadłościan
a = float(input("a: "))  # 2
b = float(input("b: "))  # 3
c = float(input("c: "))  # 4

# # Ostroslup
d_pyramid = float(input("d (ostroslup): "))  # 2
h_pyramid = float(input("h (ostroslup): "))  # 4

# Cylinder
r_cylinder = float(input("r (cylinder): "))  # 3
h_cylinder = float(input("h (cylinder): "))  # 2

# Stożek
r_cone = float(input("r (stozek): "))
h_cone = float(input("h (stozek): "))


renderer = Renderer("zadanie2.py")
renderer.render(objects)
