from time import sleep
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import numpy as np
from renderer import Renderer


stop_rotating = False


def rotate_x(theta):
    return np.array(
        [
            [1, 0, 0],
            [0, math.cos(theta), -math.sin(theta)],
            [0, math.sin(theta), math.cos(theta)],
        ]
    )


def rotate_y(theta):
    return np.array(
        [
            [math.cos(theta), 0, math.sin(theta)],
            [0, 1, 0],
            [-math.sin(theta), 0, math.cos(theta)],
        ]
    )


def rotate_z(theta):
    return np.array(
        [
            [math.cos(theta), -math.sin(theta), 0],
            [math.sin(theta), math.cos(theta), 0],
            [0, 0, 1],
        ]
    )


def rotating_cube(x_angle, y_angle, z_angle):
    a_new = a / 2
    b_new = b / 2
    c_new = c / 2
    global stop_rotating

    vertices = np.array(
        [
            [a_new, -c_new, -b_new],
            [a_new, c_new, -b_new],
            [-a_new, c_new, -b_new],
            [-a_new, -c_new, -b_new],
            [a_new, -c_new, b_new],
            [a_new, c_new, b_new],
            [-a_new, -c_new, b_new],
            [-a_new, c_new, b_new],
        ]
    )

    quads = (
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (2, 3, 7, 6),
        (0, 3, 6, 4),
        (1, 2, 7, 5),
    )
    colors = (
        (0.5, 0.5, 0.5),
        (0.5, 0.5, 0.5),
        (0.5, 0.5, 0.5),
        (0.5, 0.5, 0.5),
        (0.0, 0.5, 0.0),
        (0.0, 0.5, 0.0),
    )

    vertices = np.dot(vertices, rotate_x(x_angle))

    vertices = np.dot(vertices, rotate_y(y_angle))

    vertices = np.dot(vertices, rotate_z(z_angle))

    glPushMatrix()
    gluPerspective(45, (display[0] / display[1]), 0.1, 70.0)
    glTranslatef(15, 0, -50)
    glRotatef(45, 0, 1, 1)
    glBegin(GL_QUADS)
    for i, quad in enumerate(quads):
        glColor3f(colors[i][0], colors[i][1], colors[i][2])
        for j, vertex in enumerate(quad):
            glVertex3fv(vertices[vertex])
    glEnd()
    glPopMatrix()
    glPushMatrix()
    gluPerspective(45, (display[0] / display[1]), 0.1, 70.0)
    glTranslatef(15, 0, -50)
    glRotatef(45, 0, 1, 1)
    glBegin(GL_LINES)
    glColor3f(0.0, 0.5, 0.0)
    for i, quad in enumerate(quads):
        for j, vertex in enumerate(quad):
            glVertex3fv(vertices[vertex])
    glEnd()
    glPopMatrix()


def rotating_pyramid(d, h, x_angle, y_angle, z_angle):
    d_new = h / 2
    triangle_h = math.sqrt(3) / 2 * d
    global stop_rotating

    vertices = (
        (0.0, triangle_h, 0.0),  # Apex
        (d_new, 0.0, -d_new),
        (-d_new, 0.0, d_new),
        (0.0, 0.0, d_new * math.sqrt(3)),
    )

    quads = ((0, 1, 2), (0, 2, 3), (0, 1, 3), (0, 3, 2))

    vertices = np.dot(vertices, rotate_x(x_angle))

    vertices = np.dot(vertices, rotate_y(y_angle))

    vertices = np.dot(vertices, rotate_z(z_angle))

    glPushMatrix()
    gluPerspective(45, (display[0] / display[1]), 0.1, 70.0)
    glTranslatef(5, 0, -50)
    glRotatef(45, 0, 1, 1)
    glBegin(GL_TRIANGLES)
    for quad in quads:
        for vertex in quad:
            glVertex3fv(vertices[vertex])
    glEnd()
    glPopMatrix()


def rotating_cylinder(r, h, x_angle, y_angle, z_angle, num_segments=1000):
    vertices = []
    global stop_rotating

    for i in range(num_segments):
        angle = 2 * math.pi * i / num_segments
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        vertices.append((x, y, -h / 2))

    for i in range(num_segments):
        angle = 2 * math.pi * i / num_segments
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        vertices.append((x, y, h / 2))

    for i in range(num_segments):
        vertices.append(vertices[i])
        vertices.append(vertices[i + num_segments])

    vertices = np.dot(vertices, rotate_x(x_angle))

    vertices = np.dot(vertices, rotate_y(y_angle))

    vertices = np.dot(vertices, rotate_z(z_angle))

    glPushMatrix()
    gluPerspective(45, (display[0] / display[1]), 0.1, 70.0)
    glTranslatef(-5, 0, -50)
    glRotatef(45, 0, 1, 1)
    glBegin(GL_QUADS)
    for i in range(num_segments):
        # Dolna podstawa
        glVertex3fv(vertices[i])
        glVertex3fv(vertices[(i + 1) % num_segments])
        glVertex3fv(vertices[(i + 1) % num_segments + num_segments])
        glVertex3fv(vertices[i + num_segments])
        # Gorna podstawa
        glVertex3fv(vertices[i + num_segments])
        glVertex3fv(vertices[(i + 1) % num_segments + num_segments])
        glVertex3fv(vertices[(i + 1) % num_segments * 2])
        glVertex3fv(vertices[i + num_segments * 2])
        # Powierzchnia boczna
        glVertex3fv(vertices[i])
        glVertex3fv(vertices[(i + 1) % num_segments])
        glVertex3fv(vertices[(i + 1) % num_segments + num_segments])
        glVertex3fv(vertices[i + num_segments])
    glEnd()
    glPopMatrix()


def rotating_cone(r, h, x_angle, y_angle, z_angle, num_segments=1000):
    vertices = []
    edges = []
    global stop_rotating

    for i in range(num_segments):
        angle = 2 * math.pi * i / num_segments
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        vertices.append((x, y, -h / 2))

    vertices.append((0, 0, h / 2))

    for i in range(num_segments):
        edges.append((i, (i + 1) % num_segments))

    for i in range(num_segments):
        edges.append((i, num_segments))

    vertices = np.dot(vertices, rotate_x(x_angle))

    vertices = np.dot(vertices, rotate_y(y_angle))

    vertices = np.dot(vertices, rotate_z(z_angle))

    glBegin(GL_QUADS)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    glPushMatrix()
    gluPerspective(45, (display[0] / display[1]), 0.1, 70.0)
    glTranslatef(-15, 0, -50)
    glRotatef(45, 0, 1, 1)
    glBegin(GL_QUADS)
    for i in range(num_segments):
        glVertex3fv(vertices[i])
        glVertex3fv(vertices[(i + 1) % num_segments])
        glVertex3fv(vertices[-1])
        glVertex3fv(vertices[i])
    glEnd()
    glPopMatrix()


x_angle = 0
y_angle = 0
z_angle = 0


def rotating_objects():
    rotating_cube(x_angle, y_angle, z_angle)
    rotating_pyramid(d_pyramid, h_pyramid, x_angle, y_angle, z_angle)
    rotating_cylinder(r_cylinder, h_cylinder, x_angle, y_angle, z_angle)
    rotating_cone(r_cone, h_cone, x_angle, y_angle, z_angle)


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


def keyboard_interrupt(k, x, y):
    global stop_rotating
    stop_rotating = not stop_rotating


display = (800, 600)

# Prostopadłościan
a = float(input("a: "))
b = float(input("b: "))
c = float(input("c: "))

# Ostroslup
d_pyramid = float(input("d (ostroslup): "))
h_pyramid = float(input("h (ostroslup): "))

# Cylinder
r_cylinder = float(input("r (cylinder): "))
h_cylinder = float(input("h (cylinder): "))

# Stożek
r_cone = float(input("r (stozek): "))
h_cone = float(input("h (stozek): "))

renderer = Renderer("zadanie3.py")
renderer.render(rotating_objects, spin, keyboard_interrupt)
