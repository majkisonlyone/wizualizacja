import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from renderer import RenderOptions

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
        mat = np.zeros(3, [("pos", np.float32, 3)])
        mat['pos'] = (
                (1.0, 0.0, 0.0),
                (0.0, math.cos(theta), -math.sin(theta)),
                (0.0, math.sin(theta), math.cos(theta)),
        )
        return mat["pos"]

    def rotate_y(self, theta):
        mat = np.zeros(3, [("pos", np.float32, 3)])
        mat['pos'] = (
                (math.cos(theta), 0.0, math.sin(theta)),
                (0.0, 1.0, 0.0),
                (-math.sin(theta), 0.0, math.cos(theta)),
        )
        return mat["pos"]

    def rotate_z(self, theta):
        mat = np.zeros(3, [("pos", np.float32, 3)])
        mat['pos'] = (
                (math.cos(theta), -math.sin(theta), 0.0),
                (math.sin(theta), math.cos(theta), 0.0),
                (0.0, 0.0, 1.0))
        return mat["pos"]

    def rotate_vertices(self, vertices, angle):
        verts = np.dot(vertices["pos"], self.rotate_x(angle[0]))
        verts = np.dot(verts, self.rotate_y(angle[1]))
        verts = np.dot(verts, self.rotate_z(angle[2]))
        vertices['pos'] = verts
        return vertices

    def translate(self, vertices):
        for vert in vertices["pos"]:
            vert[0] += self.x
            vert[1] += self.y
            vert[2] += self.z
        return vertices
        


class Cube(Figure):
    def display(self):
        a_new = 0.07
        b_new = 0.1
        c_new = 0.05
        verts = np.zeros(8, [("pos", np.float32, 3), ("col", np.float32, 4)])

        verts['pos'] = [
            (a_new, -c_new, -b_new),
            (a_new, c_new, -b_new),
            (-a_new, c_new, -b_new),
            (-a_new, -c_new, -b_new),
            (a_new, -c_new, b_new),
            (a_new, c_new, b_new),
            (-a_new, c_new, b_new),
            (-a_new, -c_new, b_new)]

        verts['col'] = [
            self.color,
            self.color,
            self.color,
            self.color,
            self.color,
            self.color,
            self.color,
            self.color,
        ]

        inds = np.zeros(24, [("vals", np.int32)])
        inds["vals"] = [
            0, 1, 2, 3,
            4, 5, 6, 7,
            0, 1, 5, 4,
            1, 2, 6, 5,
            2, 3, 7, 6,
            0, 3, 7, 4
        ]

        vertices = self.rotate_vertices(verts, self.angle)
        vertices = self.translate(vertices)
        return RenderOptions(vertices,8,inds,6,GL_QUADS)

class Pyramid(Figure):
    def display(self):
        d_new = 0.2
        triangle_h = math.sqrt(3) / 2 * 0.3
        verts= np.zeros(4, [("pos", np.float32, 3), ("col", np.float32, 4)])
        verts['pos']= (
            (0.0, triangle_h, 0.0),  # Apex
            (d_new, 0.0, -d_new),
            (-d_new, 0.0, d_new),
            (0.0, 0.0, d_new * math.sqrt(3)),
        )
 
        verts['col'] = [
            self.color,
            self.color,
            self.color,
            self.color,
           ]
        inds = np.zeros(12, [("vals", np.int32)])
        inds["vals"] = [
            0, 1, 2,
            0, 2, 3,
            0, 1, 3,
            0, 3, 2]

        vertices = self.rotate_vertices(verts, self.angle)
        vertices = self.translate(vertices)
        return RenderOptions(vertices,4,inds,4,GL_TRIANGLES)

class Cone(Figure):
    r = 0.2
    h = 0.3

    def display(self):
        num_segments = 100 #0-99

        verts= np.zeros(num_segments+2, [("pos", np.float32, 3), ("col", np.float32, 4)])

        for i in range(num_segments): #okreg
            angle = 2 * math.pi * i / num_segments
            x = self.r * math.cos(angle)
            y = self.r * math.sin(angle)
            verts["pos"][i] = (x, y, -self.h / 2)
            verts["col"][i] = self.color

        verts["pos"][num_segments] = (0, 0, self.h / 2)      #wierzchołek
        verts["col"][num_segments] = (1, 1, 1, 1) 

        verts["pos"][num_segments+1] = (0, 0, -self.h / 2)   #srodek okregu
        verts["col"][num_segments+1] = (0, 0, 0, 1)

        inds = np.zeros(num_segments * 6, [("vals", np.int32)])
        
        temp_inds = []
        for i in range(num_segments - 1):       #generacja pow. bocznej
            temp_inds.append(i)
            temp_inds.append(i + 1)
            temp_inds.append(num_segments)
        temp_inds.append(num_segments - 1)
        temp_inds.append(num_segments)
        temp_inds.append(0)

        for i in range(num_segments - 1):        #generacja pow. podstawy
            temp_inds.append(i)
            temp_inds.append(i + 1)
            temp_inds.append(num_segments + 1)
        temp_inds.append(num_segments - 1)
        temp_inds.append(num_segments + 1)
        temp_inds.append(0)

        inds["vals"] = temp_inds

        vertices = self.rotate_vertices(verts, self.angle)
        vertices = self.translate(vertices)
        return RenderOptions(vertices,num_segments + 2,inds, num_segments *  6, GL_TRIANGLES)


class Cylinder(Figure):
    r = 0.2
    h = 0.4

    def display(self):
        num_segments = 100

        verts= np.zeros(2 * (num_segments+1), [("pos", np.float32, 3), ("col", np.float32, 4)])
        
        for i in range(num_segments): #okreg 1 indeksy 0 - 99
            angle = 2 * math.pi * i / num_segments
            x = self.r * math.cos(angle)
            y = self.r * math.sin(angle)
            verts["pos"][i] = (x, y, -self.h / 2)
            verts["col"][i] = self.color

        for i in range(num_segments): #okreg 2 indeksy 100 - 199
            angle = 2 * math.pi * i / num_segments
            x = self.r * math.cos(angle)
            y = self.r * math.sin(angle)
            verts["pos"][num_segments + i] = (x, y, self.h / 2)
            verts["col"][num_segments + i] = self.color

        verts["pos"][2 * num_segments] = (0, 0, -self.h / 2)         #srodek okregu 1
        verts["col"][2 * num_segments] = (0, 0, 0, 1)

        verts["pos"][2 * num_segments + 1] = (0, 0, self.h / 2)      #srodek okregu 2
        verts["col"][2 * num_segments + 1] = (1, 1, 1, 1) 

        inds = np.zeros(num_segments * 12, [("vals", np.int32)])

        temp_inds = []
        for i in range(num_segments - 1):       #generacja pow. bocznej
            temp_inds.append(i)
            temp_inds.append(i + 1)
            temp_inds.append(num_segments + i)
            temp_inds.append(num_segments)
            temp_inds.append(num_segments + i +1)
            temp_inds.append(i + 1)

        temp_inds.append(2 * num_segments - 1)
        temp_inds.append(num_segments -1)
        temp_inds.append(0) 
        temp_inds.append(2 * num_segments - 1)
        temp_inds.append(num_segments)
        temp_inds.append(0) 

        for i in range(num_segments - 1):        #generacja pow. podstawy 1
            temp_inds.append(i)
            temp_inds.append(i + 1)
            temp_inds.append(2 * num_segments)
        temp_inds.append(num_segments - 1)
        temp_inds.append(2 * num_segments)
        temp_inds.append(0)

        for i in range(num_segments - 1):        #generacja pow. podstawy 1
            temp_inds.append(num_segments + i)
            temp_inds.append(num_segments + i + 1)
            temp_inds.append(2 * num_segments + 1)
        temp_inds.append(2 * num_segments - 1)
        temp_inds.append(2 * num_segments + 1)
        temp_inds.append(num_segments)

        inds["vals"] = temp_inds
        
        vertices = self.rotate_vertices(verts, self.angle)
        vertices = self.translate(vertices)
        return RenderOptions(vertices, 2 * num_segments + 2,inds, num_segments *  12, GL_TRIANGLES)

class Sphere(Figure):
    r = 0.5
    precision = 1
    num_circles = pow(2, precision)
    num_segments = 2 * num_circles
    angle_between_circs = math.pi/num_circles
    verts_len = num_segments * num_circles
    inds_len = verts_len * 3
    
    def display(self):
        circles_list = []

        for circle_id in range(self.num_circles):    #generowanie listy okregow
            single_circ_verts = np.zeros(self.num_segments, [("pos", np.float32, 3), ("col", np.float32, 4)])
            
            for i in range(self.num_segments):      #generowanie pojedynczego okregu
                angle = 2 * math.pi * i / self.num_segments
                x = self.r * math.cos(angle)
                y = self.r * math.sin(angle)
                print("pos"+str(i)+" x="+str(x)+" y="+str(y))
                single_circ_verts["pos"][i] = (x, y, 0)
                single_circ_verts["col"][i] = self.color

            vertices = self.rotate_vertices(single_circ_verts, [0,self.angle_between_circs * circle_id,0])      #obracanie okregow o dany kat wzgledem siebie
            circles_list.append(vertices)      #wpisywanie punktow okregu na liste jako okreg 0, 1, 2 itd.
        print("MYLOG len circ_list " + str(len(circles_list)))
        circles_verts = len(circles_list) * self.num_circles

        verts = np.zeros(self.verts_len, [("pos", np.float32, 3), ("col", np.float32, 4)])
        itera = 0
        for single_circ_verts in circles_list:
            for i in range(len(single_circ_verts)):
                verts["pos"][itera] = single_circ_verts["pos"][i]
                verts["col"][itera] = single_circ_verts["col"][i]
                itera += 1

        for i,vert in enumerate(verts["pos"]):
            print("pos vert " +str(i)+" x="+str(vert[0])+" y="+str(vert[1])+" z"+str(vert[2]))
        
        temp_inds = []
        for circle_id in range(self.num_circles - 1):    #generacja polaczen okregow
            itera = 0
            for i in range(self.num_segments):
                temp_inds.append(i + itera*self.num_segments) #0
                temp_inds.append(i + itera*self.num_segments + 1) #1
                temp_inds.append(self.num_segments + i + itera*self.num_segments) #4

                temp_inds.append(self.num_segments + i + itera*self.num_segments) #4
                temp_inds.append(self.num_segments + i + itera*self.num_segments + 1) #5
                temp_inds.append(i + itera*self.num_segments + 1) #1
            temp_inds.append(2 * self.num_segments - 1 + itera*self.num_segments)
            temp_inds.append(self.num_segments - 1 + itera*self.num_segments)
            temp_inds.append(itera*self.num_segments)
            temp_inds.append(2 * self.num_segments - 1 + itera*self.num_segments)
            temp_inds.append(self.num_segments + itera*self.num_segments)
            temp_inds.append(itera*self.num_segments)
            itera += self.num_segments
        print("MYLOG len inds " + str(len(temp_inds)))
        inds = np.zeros(len(temp_inds), [("vals", np.int32)])

        for i in temp_inds:
            inds["vals"][i] = temp_inds[i]







        
        
        # for i in range(num_segments): #okreg 1 indeksy 0 - 99
        #     angle = 2 * math.pi * i / num_segments
        #     x = self.r * math.cos(angle)
        #     y = self.r * math.sin(angle)
        #     verts["pos"][i] = (x, y, -self.h / 2)
        #     verts["col"][i] = self.color

        # for i in range(num_segments): #okreg 2 indeksy 100 - 199
        #     angle = 2 * math.pi * i / num_segments
        #     x = self.r * math.cos(angle)
        #     y = self.r * math.sin(angle)
        #     verts["pos"][num_segments + i] = (x, y, self.h / 2)
        #     verts["col"][num_segments + i] = self.color

        # verts["pos"][2 * num_segments] = (0, 0, -self.h / 2)         #srodek okregu 1
        # verts["col"][2 * num_segments] = (0, 0, 0, 1)

        # verts["pos"][2 * num_segments + 1] = (0, 0, self.h / 2)      #srodek okregu 2
        # verts["col"][2 * num_segments + 1] = (1, 1, 1, 1) 

        # inds = np.zeros(num_segments * 12, [("vals", np.int32)])

        # temp_inds = []
        # for i in range(num_segments - 1):       #generacja pow. bocznej
        #     temp_inds.append(i)
        #     temp_inds.append(i + 1)
        #     temp_inds.append(num_segments + i)
        #     temp_inds.append(num_segments)
        #     temp_inds.append(num_segments + i +1)
        #     temp_inds.append(i + 1)

        # temp_inds.append(2 * num_segments - 1)
        # temp_inds.append(num_segments -1)
        # temp_inds.append(0) 
        # temp_inds.append(2 * num_segments - 1)
        # temp_inds.append(num_segments)
        # temp_inds.append(0) 

        # for i in range(num_segments - 1):        #generacja pow. podstawy 1
        #     temp_inds.append(i)
        #     temp_inds.append(i + 1)
        #     temp_inds.append(2 * num_segments)
        # temp_inds.append(num_segments - 1)
        # temp_inds.append(2 * num_segments)
        # temp_inds.append(0)

        # for i in range(num_segments - 1):        #generacja pow. podstawy 1
        #     temp_inds.append(num_segments + i)
        #     temp_inds.append(num_segments + i + 1)
        #     temp_inds.append(2 * num_segments + 1)
        # temp_inds.append(2 * num_segments - 1)
        # temp_inds.append(2 * num_segments + 1)
        # temp_inds.append(num_segments)

        # inds["vals"] = temp_inds
        
        # vertices = self.rotate_vertices(verts, self.angle)
        vertices = self.translate(vertices)
        return RenderOptions(vertices, self.verts_len,inds, self.inds_len, GL_TRIANGLES)
