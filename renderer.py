from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.GL.shaders import compileProgram, compileShader

vsc = """
attribute vec3 position;
void main() {
gl_Position = vec4(position, 1.0);
} """
fsc = """
#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;

void main() {
	vec2 st = gl_FragCoord.xy/u_resolution;
	gl_FragColor = vec4(st.x,st.y,0.0,1.0);
}"""


class Renderer:
    def __init__(self, name):
        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
        glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(name)
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Kolor tła
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)

    def render(self, func):
        def function():
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glColor3f(1.0, 1.0, 1.0)
            glLoadIdentity()
            func()
            glutSwapBuffers()
            glFlush()

        glutDisplayFunc(function)
        glutMainLoop()

    def render(self, disp, idle, keyboard):
        def display():
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glColor3f(1.0, 1.0, 1.0)
            glLoadIdentity()
            disp()
            glutSwapBuffers()
            glFlush()

        glutDisplayFunc(display)
        glutIdleFunc(idle)
        glutKeyboardFunc(keyboard)
        glutMainLoop()

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

    def _prerender(self):
        verts = np.zeros(3, [("position", np.float32, 3)])
        verts["position"] = [(-1, -1, 0), (1, -1, 0), (1, 1, 0)]
        buf = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buf)
        glBufferData(GL_ARRAY_BUFFER, verts.nbytes, verts, GL_STATIC_DRAW)
        width = verts.strides[0]
        offset = ctypes.c_void_p(0)
        position = glGetAttribLocation(self.shader, "position")
        glEnableVertexAttribArray(position)
        glBindBuffer(GL_ARRAY_BUFFER, buf)
        glVertexAttribPointer(position, 3, GL_FLOAT, False, width, offset)

    def render_with_shader(self, disp):
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        def display():
            disp()
            glutSwapBuffers()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glutDisplayFunc(display)
        self._shade()
        self._prerender()
        glutMainLoop()
