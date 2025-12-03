import math as mt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

vsc = """
attribute vec3 pozycja;
attribute vec4 kolor;
varying vec4 frag_kolor;
//uniform mat4 transl_mat;
void main() {
gl_Position = vec4(pozycja, 1.0);
frag_kolor = kolor;
} """
fsc = """
varying vec4 frag_kolor;
void main() {
gl_FragColor = frag_kolor;
} """

vsc_cam_m_v_p = """
#version 330 core
layout (location = 0) in vec3 pozycja;
layout (location = 1) in vec4 kolor;
//uniform mat4 mvp;
uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;
out vec4 frag_kolor;
void main() {
gl_Position = projection * view * model * vec4(pozycja, 1.0);
frag_kolor = kolor;
} """

vsc_cam_mvp = """
#version 330 core
layout (location = 0) in vec3 pozycja;
layout (location = 1) in vec4 kolor;
uniform mat4 mvp;
out vec4 frag_kolor;
void main() {
gl_Position = mvp * vec4(pozycja, 1.0);
frag_kolor = kolor;
} """


class RenderedObject:
    def __init__(self, vao, inds, length, draw_option):
        self.vao = vao
        self.length = length
        self.draw_option = draw_option
        self.inds = inds


class RenderOptions:
    def __init__(self, verts, vert_len, inds, inds_len, draw_option):
        self.verts = verts
        self.vert_len = vert_len
        self.inds = inds
        self.inds_len = inds_len
        self.draw_option = draw_option


class CameraOptions:
    def __init__(self, near=1, far=10, left=-1, right=1, bottom=-1, top=1):
        self.near = near
        self.far = far
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top


class CameraOrientation:
    def __init__(self, dist=2, angl_left_right=0, angl_top_bot=0):
        self.dist = dist
        self.angl_left_right = angl_left_right
        self.angl_top_bot = angl_top_bot


class Renderer:
    camera_options = CameraOptions()
    camera_orientation = CameraOrientation()

    def __init__(self, name):
        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(name)
        glClearColor(0.1, 0.1, 0.1, 1.0)  # Kolor tła
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        self.rendered_objects = []

    def _shade(self):
        self.shader = glCreateProgram()
        vshader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vshader, vsc)
        glCompileShader(vshader)
        if not glGetShaderiv(vshader, GL_COMPILE_STATUS):
            print("v:" + str(glGetShaderInfoLog(vshader).decode()))
        fshader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fshader, fsc)
        glCompileShader(fshader)
        if not glGetShaderiv(fshader, GL_COMPILE_STATUS):
            print("f:" + str(glGetShaderInfoLog(fshader).decode()))
        glAttachShader(self.shader, vshader)
        glAttachShader(self.shader, fshader)
        glLinkProgram(self.shader)
        if not glGetProgramiv(self.shader, GL_LINK_STATUS):
            print("p:" + str(glGetProgramInfoLog(self.shader)))
        glUseProgram(self.shader)
        glDetachShader(self.shader, vshader)
        glDetachShader(self.shader, fshader)

    def _shade_cam(self, vsc_type):
        self.shader = glCreateProgram()
        vshader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vshader, vsc_type)
        glCompileShader(vshader)
        if not glGetShaderiv(vshader, GL_COMPILE_STATUS):
            print("v:" + str(glGetShaderInfoLog(vshader).decode()))
        fshader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fshader, fsc)
        glCompileShader(fshader)
        if not glGetShaderiv(fshader, GL_COMPILE_STATUS):
            print("f:" + str(glGetShaderInfoLog(fshader).decode()))
        glAttachShader(self.shader, vshader)
        glAttachShader(self.shader, fshader)
        glLinkProgram(self.shader)
        if not glGetProgramiv(self.shader, GL_LINK_STATUS):
            print("p:" + str(glGetProgramInfoLog(self.shader)))
        glUseProgram(self.shader)
        glDetachShader(self.shader, vshader)
        glDetachShader(self.shader, fshader)

    def _prerender(self, render_options):
        for render in render_options:
            temp_vao = glGenVertexArrays(1)
            glBindVertexArray(temp_vao)
            buf = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, buf)
            glBufferData(
                GL_ARRAY_BUFFER, render.verts.nbytes, render.verts, GL_STATIC_DRAW
            )
            width = render.verts.strides[0]
            offset = ctypes.c_void_p(0)
            position = glGetAttribLocation(self.shader, "pozycja")
            glEnableVertexAttribArray(position)
            glBindBuffer(GL_ARRAY_BUFFER, buf)
            glVertexAttribPointer(position, 3, GL_FLOAT, False, width, offset)
            offset = ctypes.c_void_p(render.verts.dtype["pos"].itemsize)
            color = glGetAttribLocation(self.shader, "kolor")
            glEnableVertexAttribArray(color)
            glBindBuffer(GL_ARRAY_BUFFER, buf)
            glVertexAttribPointer(color, 4, GL_FLOAT, False, width, offset)
            ebo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, ebo)
            glBufferData(
                GL_ARRAY_BUFFER, render.inds.nbytes, render.inds, GL_STATIC_DRAW
            )
            glBindVertexArray(0)
            # print("prerend")
            self.rendered_objects.append(
                RenderedObject(
                    temp_vao, render.inds, len(render.inds), render.draw_option
                )
            )

    def _prerender_cam_per(self, render_options):
        for render in render_options:
            temp_vao = glGenVertexArrays(1)
            glBindVertexArray(temp_vao)
            buf = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, buf)
            glBufferData(
                GL_ARRAY_BUFFER, render.verts.nbytes, render.verts, GL_STATIC_DRAW
            )
            width = render.verts.strides[0]
            offset = ctypes.c_void_p(0)
            position = glGetAttribLocation(self.shader, "pozycja")
            glEnableVertexAttribArray(position)
            glBindBuffer(GL_ARRAY_BUFFER, buf)
            glVertexAttribPointer(position, 3, GL_FLOAT, False, width, offset)

            offset = ctypes.c_void_p(render.verts.dtype["pos"].itemsize)
            color = glGetAttribLocation(self.shader, "kolor")
            glEnableVertexAttribArray(color)
            glBindBuffer(GL_ARRAY_BUFFER, buf)
            glVertexAttribPointer(color, 4, GL_FLOAT, False, width, offset)

            mvp = glGetUniformLocation(self.shader, "mvp")
            near = self.camera_options.near
            far = self.camera_options.far
            left = self.camera_options.left
            right = self.camera_options.right
            bottom = self.camera_options.bottom
            top = self.camera_options.top
            mvpmat1 = np.array(  # macierz pers proj
                [
                    [2 * near / (right - left), 0, (right + left) / (right - left), 0],
                    [0, 2 * near / (top - bottom), (top + bottom) / (top - bottom), 0],
                    [0, 0, -(far + near) / (far - near), -2 * far * near / (far - near)],
                    [0, 0, -1, 0],
                ],
                dtype=np.float32,
            )
            x = (
                self.camera_orientation.dist
                * mt.cos(self.camera_orientation.angl_left_right)
                * mt.cos(self.camera_orientation.angl_top_bot)
            )
            y = self.camera_orientation.dist * mt.sin(
                self.camera_orientation.angl_top_bot
            )
            z = (
                self.camera_orientation.dist
                * mt.sin(self.camera_orientation.angl_left_right)
                * mt.cos(self.camera_orientation.angl_top_bot)
            )
            xyz = np.array([x, y, z], dtype=np.float32)
            target = np.array([0, 0, 0], dtype=np.float32)
            direction = xyz - target
            direction = direction / np.linalg.norm(direction)
            up = np.array([0, 1, 0], dtype=np.float32)
            right = np.cross(direction, up)
            up = np.cross(right, direction)
            mvpmat2 = np.array(
                [
                    [1, 0, 0, -xyz[0]],
                    [0, 1, 0, -xyz[1]],
                    [0, 0, 1, -xyz[2]],
                    [0, 0, 0, 1],
                ],
                dtype=np.float32,
            )
            mvpmat3 = np.array(
                [
                    [right[0], right[1], right[2], 0],
                    [up[0], up[1], up[2], 0],
                    [direction[0], direction[1], direction[2], 0],
                    [0, 0, 0, 1],
                ],
                dtype=np.float32,
            )
            mvpmat = np.matmul(mvpmat3, mvpmat2)
            mvpmat = np.matmul(mvpmat1, mvpmat)
            mvpmat = mvpmat.transpose()
            glUniformMatrix4fv(mvp, 1, False, mvpmat.flatten("C"))

            ebo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, ebo)
            glBufferData(
                GL_ARRAY_BUFFER, render.inds.nbytes, render.inds, GL_STATIC_DRAW
            )
            glBindVertexArray(0)
            self.rendered_objects.append(
                RenderedObject(
                    temp_vao, render.inds, len(render.inds), render.draw_option
                )
            )

    def _prerender_cam_ort2(self, render_options):
        for render in render_options:
            temp_vao = glGenVertexArrays(1)
            glBindVertexArray(temp_vao)
            buf = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, buf)
            glBufferData(
                GL_ARRAY_BUFFER, render.verts.nbytes, render.verts, GL_STATIC_DRAW
            )
            width = render.verts.strides[0]
            offset = ctypes.c_void_p(0)
            position = glGetAttribLocation(self.shader, "pozycja")
            glEnableVertexAttribArray(position)
            glBindBuffer(GL_ARRAY_BUFFER, buf)
            glVertexAttribPointer(position, 3, GL_FLOAT, False, width, offset)

            offset = ctypes.c_void_p(render.verts.dtype["pos"].itemsize)
            color = glGetAttribLocation(self.shader, "kolor")
            glEnableVertexAttribArray(color)
            glBindBuffer(GL_ARRAY_BUFFER, buf)
            glVertexAttribPointer(color, 4, GL_FLOAT, False, width, offset)

            mvp = glGetUniformLocation(self.shader, "mvp")
            near = self.camera_options.near
            far = self.camera_options.far
            left = 0.2 * self.camera_options.left
            right = 0.2 * self.camera_options.right
            bottom = self.camera_options.bottom
            top = self.camera_options.top
            # orth dokumentacja: https://learnwebgl.brown37.net/08_projections/projections_ortho.html
            mvpmat1 = np.array(
                [
                    [2 * (right - left), 0, 0, -(right + left) / (right - left)],
                    [0, 2 / (top - bottom), 0, -(top + bottom) / (top - bottom)],
                    [0, 0, -2 / (far - near), -(far + near) / (far - near)],
                    [0, 0, 0, 1],
                ],
                dtype=np.float32,
            )
            x = (
                self.camera_orientation.dist
                * mt.cos(self.camera_orientation.angl_left_right)
                * mt.cos(self.camera_orientation.angl_top_bot)
            )
            y = self.camera_orientation.dist * mt.sin(
                self.camera_orientation.angl_top_bot
            )
            z = (
                self.camera_orientation.dist
                * mt.sin(self.camera_orientation.angl_left_right)
                * mt.cos(self.camera_orientation.angl_top_bot)
            )
            xyz = np.array([x, y, z], dtype=np.float32)
            target = np.array([0, 0, 0], dtype=np.float32)
            direction = xyz - target
            direction = direction / np.linalg.norm(direction)
            up = np.array([0, 1, 0], dtype=np.float32)
            right = np.cross(direction, up)
            up = np.cross(right, direction)
            mvpmat2 = np.array(
                [
                    [1, 0, 0, -xyz[0]],
                    [0, 1, 0, -xyz[1]],
                    [0, 0, 1, -xyz[2]],
                    [0, 0, 0, 1],
                ],
                dtype=np.float32,
            )
            mvpmat3 = np.array(
                [
                    [right[0], right[1], right[2], 0],
                    [up[0], up[1], up[2], 0],
                    [direction[0], direction[1], direction[2], 0],
                    [0, 0, 0, 1],
                ],
                dtype=np.float32,
            )
            mvpmat = np.matmul(mvpmat3, mvpmat2)
            mvpmat = np.matmul(mvpmat1, mvpmat)
            mvpmat = mvpmat.transpose()
            glUniformMatrix4fv(mvp, 1, False, mvpmat.flatten("C"))

            ebo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, ebo)
            glBufferData(
                GL_ARRAY_BUFFER, render.inds.nbytes, render.inds, GL_STATIC_DRAW
            )
            glBindVertexArray(0)
            self.rendered_objects.append(
                RenderedObject(
                    temp_vao, render.inds, len(render.inds), render.draw_option
                )
            )

    def show(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for obj in self.rendered_objects:
            glBindVertexArray(obj.vao)
            glDrawElements(obj.draw_option, obj.length, GL_UNSIGNED_INT, obj.inds)
        glutSwapBuffers()

    def reshape(self, w, h):
        glViewport(0, 0, w, h)

    def render_with_shader(
        self, render_options: list[RenderOptions], idle=None, keyboard=None
    ):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glutDisplayFunc(self.show)
        glutReshapeFunc(self.reshape)
        self._shade()
        self._prerender(render_options)
        if idle is not None:
            # print("idle")
            glutIdleFunc(idle)
        if keyboard is not None:
            # print("keyboard")
            glutKeyboardFunc(keyboard)
        glutMainLoop()

    def render_with_shader_rot(self, render_options_func, idle=None, keyboard=None):
        def display():
            self.rendered_objects = []
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self._shade()
            self._prerender(render_options_func())
            for obj in self.rendered_objects:
                glBindVertexArray(obj.vao)
                glDrawElements(obj.draw_option, obj.length, GL_UNSIGNED_INT, obj.inds)
            glutSwapBuffers()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glutDisplayFunc(display)
        glutReshapeFunc(self.reshape)

        if idle is not None:
            # print("idle")
            glutIdleFunc(idle)
        if keyboard is not None:
            # print("keyboard")
            glutKeyboardFunc(keyboard)
        glutMainLoop()

    def render_with_shader_rot_cam(
        self, cam_type, render_options_func, idle=None, keyboard=None
    ):
        def display():
            self.rendered_objects = []
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            if cam_type == "orth":
                self._shade_cam(vsc_cam_mvp)
                self._prerender_cam_ort2(render_options_func())
            if cam_type == "pers":
                self._shade_cam(vsc_cam_mvp)
                self._prerender_cam_per(render_options_func())
            for obj in self.rendered_objects:
                glBindVertexArray(obj.vao)
                glDrawElements(obj.draw_option, obj.length, GL_UNSIGNED_INT, obj.inds)
            glutSwapBuffers()

        def keyboard2(k, x, y):
            if k == b"w":
                self.camera_orientation.dist -= 0.1
            if k == b"s":
                self.camera_orientation.dist += 0.1
            if k == b"a":
                self.camera_orientation.angl_left_right += 0.1
            if k == b"d":
                self.camera_orientation.angl_left_right -= 0.1
            if k == b"r":
                self.camera_orientation.angl_top_bot += 0.1
            if k == b"f":
                self.camera_orientation.angl_top_bot -= 0.1
            if k == b"c":
                self.camera_options.near = float(
                    input("Podaj near (sugestia od 0.1 do 1): ")
                )
                self.camera_options.far = float(
                    input("Podaj far (sugestia od 5 do 10): ")
                )
                self.camera_options.top = float(
                    input("Podaj top (sugestia od 1 do 2): ")
                )
                self.camera_options.bottom = float(
                    input("Podaj bottom (sugestia od -1 do -2): ")
                )
                self.camera_options.left = float(
                    input("Podaj left (sugestia od -1 do -2): ")
                )
                self.camera_options.right = float(
                    input("Podaj right (sugestia od 1 do 2): ")
                )
            if k == b"p":
                self.camera_options = CameraOptions()
            if k == b"q":
                glutLeaveMainLoop()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glutDisplayFunc(display)
        glutReshapeFunc(self.reshape)

        if idle is not None:
            # print("idle")
            glutIdleFunc(idle)
        if keyboard is not None:
            # print("keyboard")
            glutKeyboardFunc(keyboard2)
        glutMainLoop()
