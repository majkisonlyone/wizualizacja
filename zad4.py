from typing import Dict
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import numpy as np
from renderer import Renderer
from figures import Figure,Cube,Pyramid,Cone,Cylinder

objects = []

def rotating_objects():
    for object in objects:
        object.display()

def spin():
    glutPostRedisplay()

def keyboard_interrupt(key, x, y):
    if key == b'a':
        print("Dodaawnie bryly...")
        x = int(input("Podaj x (sugestia od -20 do 20): "))
        y = int(input("Podaj y (sugestia = 0): "))
        z = int(input("Podaj z (sugestia = -50): "))
        color = int(input("Podaj kolor (0-czerwony, 1-zielony, 2-niebieski): "))
        x_angle = int(input("Podaj kat obrotu wzgledem osi x: "))
        y_angle = int(input("Podaj kat obrotu wzgledem osi y: "))
        z_angle = int(input("Podaj kat obrotu wzgledem osi z: "))
        colors = [
        (1, 0, 0),  # Red
        (0, 1, 0),  # Green
        (0, 0, 1),  # Blue
        (1, 1, 0),  # Yellow
        (1, 0, 1),  # Magenta
        (0, 1, 1),  # Cyan
        (1, 1, 1),  # White
        (0.5, 0.5, 0.5)  # Gray
        ]
        type = int(input("Dodaj 1->Prostopadloscian, 2->Ostroslup, 3->Cylinder, 4->Stozek: "))
        if type == 1:
            objects.append(Cube(x, y, z, colors[color], (x_angle, y_angle, z_angle)))
        if type == 2:
            objects.append(Pyramid(x, y, z, colors[color], (x_angle, y_angle, z_angle)))
        if type == 3:
            objects.append(Cylinder(x, y, z, colors[color], (x_angle, y_angle, z_angle)))
        if type == 4:
            objects.append(Cone(x, y, z, colors[color], (x_angle, y_angle, z_angle)))

    if key == b'd':
        for object in objects:
            print("Obiekt " + str(object.id))
        id_to_remove = int(input("Usun obiekt o id: "))
        for object in objects:
            if object.id == id_to_remove:
                objects.remove(object)
    glutPostRedisplay()


display = (800, 600)

renderer = Renderer("zadanie3.py")
renderer.render(rotating_objects, spin, keyboard_interrupt)