from file_handler import FileReader
from renderer import *

file_reader = FileReader("file1.sci")
objects, cam_params = file_reader.read()


def rotating_objects():
    global objects, cam_params
    render_options_list = []
    for obj in objects:
        render_options_list.append(obj.display())
    return render_options_list


def spin():
    glutPostRedisplay()


def keyboard_interrupt(k, x, y):
    pass


renderer = Renderer("zadanie5_3.py")
renderer.camera_orientation = cam_params
renderer.render_with_shader_rot_cam("pers", rotating_objects, spin, keyboard_interrupt)
