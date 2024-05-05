import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import math

id = 0


class Figure:
    def __init__(self, x, y, z, color, angle):
        global id
        self.id = id + 1
        self.x = x
        self.y = y
        self.z = z
        self.color = color  # (1, 0, 0)
        self.angle = angle  # [x_angle, y_angle, z_angle]
        id = id + 1

    def display(self):
        pass

    def rotate_x(self, theta):
        return np.array(
            [
                [1, 0, 0],
                [0, math.cos(theta), -math.sin(theta)],
                [0, math.sin(theta), math.cos(theta)],
            ]
        )

    def rotate_y(self, theta):
        return np.array(
            [
                [math.cos(theta), 0, math.sin(theta)],
                [0, 1, 0],
                [-math.sin(theta), 0, math.cos(theta)],
            ]
        )

    def rotate_z(self, theta):
        return np.array(
            [
                [math.cos(theta), -math.sin(theta), 0],
                [math.sin(theta), math.cos(theta), 0],
                [0, 0, 1],
            ]
        )

    def rotate_vertices(self, vertices, angle):
        vertices = np.dot(vertices, self.rotate_x(angle[0]))
        vertices = np.dot(vertices, self.rotate_y(angle[1]))
        vertices = np.dot(vertices, self.rotate_z(angle[2]))
        return vertices


class Cube(Figure):
    def display(self):
        a_new = 1
        b_new = 2
        c_new = 3

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

        vertices = self.rotate_vertices(vertices, self.angle)

        glPushMatrix()
        gluPerspective(45, (800 / 600), 0.1, 70.0)
        glTranslatef(self.x, self.y, self.z)
        glColor3f(self.color[0], self.color[1], self.color[2])
        glBegin(GL_QUADS)
        for i, quad in enumerate(quads):
            for j, vertex in enumerate(quad):
                glVertex3fv(vertices[vertex])
        glEnd()

        glColor3f(1, 1, 1)
        glBegin(GL_LINES)
        for quad in quads:
            for vertex in quad:
                glVertex3fv(vertices[vertex])
        glEnd()
        glPopMatrix()


class Pyramid(Figure):
    def display(self):
        d_new = 2
        triangle_h = math.sqrt(3) / 2 * 3
        vertices = (
            (0.0, triangle_h, 0.0),  # Apex
            (d_new, 0.0, -d_new),
            (-d_new, 0.0, d_new),
            (0.0, 0.0, d_new * math.sqrt(3)),
        )

        quads = ((0, 1, 2), (0, 2, 3), (0, 1, 3), (0, 3, 2))

        vertices = self.rotate_vertices(vertices, self.angle)

        glPushMatrix()
        gluPerspective(45, (800 / 600), 0.1, 70.0)
        glTranslatef(self.x, self.y, self.z)
        glColor3f(self.color[0], self.color[1], self.color[2])
        glBegin(GL_TRIANGLES)
        for quad in quads:
            for vertex in quad:
                glVertex3fv(vertices[vertex])
        glEnd()

        glColor3f(1, 1, 1)
        glBegin(GL_LINES)
        for quad in quads:
            for vertex in quad:
                glVertex3fv(vertices[vertex])
        glEnd()
        glPopMatrix()


class Cone(Figure):
    def display(self):
        vertices = []
        edges = []
        r = 3
        h = 4
        num_segments = 100

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

        vertices = self.rotate_vertices(vertices, self.angle)
        glPushMatrix()
        gluPerspective(45, (800 / 600), 0.1, 70.0)
        glTranslatef(self.x, self.y, self.z)
        glColor3f(self.color[0], self.color[1], self.color[2])
        glBegin(GL_QUADS)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()

        # glColor3f(1, 1, 1)
        # glBegin(GL_LINES)
        # for edge in edges:
        #     for vertex in edge:
        #         glVertex3fv(vertices[vertex])
        # glEnd()

        glBegin(GL_QUADS)
        for i in range(num_segments):
            glVertex3fv(vertices[i])
            glVertex3fv(vertices[(i + 1) % num_segments])
            glVertex3fv(vertices[-1])
            glVertex3fv(vertices[i])
        glEnd()
        glPopMatrix()


class Cylinder(Figure):
    def display(self):
        vertices = []
        num_segments = 100
        r = 3
        h = 5

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

        vertices = self.rotate_vertices(vertices, self.angle)

        glPushMatrix()
        gluPerspective(45, (800 / 600), 0.1, 70.0)
        glTranslatef(self.x, self.y, self.z)
        glColor3f(self.color[0], self.color[1], self.color[2])
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

        # glColor3f(1, 1, 1)
        # glBegin(GL_LINES)
        # for i in range(num_segments):
        #     # Dolna podstawa
        #     glVertex3fv(vertices[i])
        #     glVertex3fv(vertices[(i + 1) % num_segments])
        #     glVertex3fv(vertices[(i + 1) % num_segments + num_segments])
        #     glVertex3fv(vertices[i + num_segments])
        #     # Gorna podstawa
        #     glVertex3fv(vertices[i + num_segments])
        #     glVertex3fv(vertices[(i + 1) % num_segments + num_segments])
        #     glVertex3fv(vertices[(i + 1) % num_segments * 2])
        #     glVertex3fv(vertices[i + num_segments * 2])
        # glEnd()
        glPopMatrix()
