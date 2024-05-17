import math
from OpenGL.GL import *
from renderer import Renderer, RenderOptions
import numpy as np



def polygon(sides, side_length):
    verts = np.zeros(sides + 1, [("pos", np.float32, 3), ("col", np.float32, 4)])
    radius = side_length / (2 * math.sin(math.pi / sides))
    verts["pos"][0] = (0, 0, 0)
    verts["col"][0] = (1.000, 0.423, 0.691, 1.000)
    for i in range(sides):
        angle = 2 * math.pi * i / sides
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        verts["pos"][i + 1] = (x, y, 0)
        # print("vert x=" + str(x) + " y=" + str(y) + " z=0")
        verts["col"][i + 1] = (0.455, 0.160, 1.000, 1.000)

    inds = np.zeros(sides * 3, [("vals", np.int32)])
    temp_inds = []
    for i in range(sides - 1):
        temp_inds.append(0)
        temp_inds.append(i + 1)
        temp_inds.append(i + 2)
    temp_inds.append(0)
    temp_inds.append(sides)
    temp_inds.append(1)
    inds["vals"] = temp_inds
    render_options = [RenderOptions(verts, len(verts), inds, len(inds), GL_TRIANGLES)]
    return render_options


sides = int(input("Podaj ilość boków N: "))
side_length = float(input("Podaj długość boku d: ")) / 10

renderer = Renderer("zadanie1.py")
renderer.render_with_shader(polygon(sides, side_length))
