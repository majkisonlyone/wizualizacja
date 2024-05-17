from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.GL.shaders import compileProgram, compileShader

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


class Renderer:
    def __init__(self, name):
        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
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

    def show(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for obj in self.rendered_objects:
            glBindVertexArray(obj.vao)
            glDrawElements(obj.draw_option, obj.length, GL_UNSIGNED_INT, obj.inds)
        glutSwapBuffers()

    def reshape(self, w, h):
        glViewport(0, 0, w, h)

    def render_with_shader(self, render_options : list[RenderOptions], idle = None, keyboard = None):
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

    def render_with_shader_rot(self, render_options_func, idle = None, keyboard = None):
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
