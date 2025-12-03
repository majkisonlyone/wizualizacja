from file_handler import FileReader
from renderer import *
from figures import *
from time import sleep

file_reader = FileReader("file1.sci")
objects, cam_params = file_reader.read()

robot_x = -0.15
robot_y = 0
robot_z = -0.5
path_ang = 0
increment = 1 / 256
robot_angle = [0, 0, 0]


class Robot:
    body = Cube(
        robot_x, robot_y, robot_z, (0.8, 0.8, 0.8, 1), robot_angle
    ).set_dimensions(float(0.3), float(0.2), float(0.2))
    wheel_1 = Cylinder(
        robot_x - 0.3 / 4, robot_y, robot_z + 0.2, (0, 0.8, 0, 1), robot_angle
    ).set_dimensions(float(0.1), float(0.1))
    wheel_2 = Cylinder(
        robot_x - 0.3 / 4, robot_y, robot_z - 0.2, (0, 0, 0.8, 1), robot_angle
    ).set_dimensions(float(0.1), float(0.1))


robot = Robot()


def render_objects():
    global objects, cam_params, robot
    render_options_list = []
    for obj in objects:
        render_options_list.append(obj.display())
    render_options_list.append(robot.body.display())
    render_options_list.append(robot.wheel_1.display())
    render_options_list.append(robot.wheel_2.display())
    return render_options_list


def move_robot():
    global robot, path_ang
    robot.body.y = 0.7 * math.sin(path_ang)
    robot.body.z = 0.7 * math.cos(path_ang)
    robot.wheel_1.y = 0.85 * math.sin(path_ang)
    robot.wheel_1.z = 0.85 * math.cos(path_ang)
    robot.wheel_2.y = 0.55 * math.sin(path_ang)
    robot.wheel_2.z = 0.55 * math.cos(path_ang)
    robot.body.angle[0] += (2 * math.pi * increment) % (2 * math.pi)

    path_ang = (path_ang + 2 * math.pi * increment) % (2 * math.pi)
    sleep(0.05)
    glutPostRedisplay()


def keyboard_interrupt(k, x, y):
    pass


renderer = Renderer("zadanie5_3.py")
renderer.camera_orientation = cam_params
renderer.render_with_shader_rot_cam(
    "pers", render_objects, move_robot, keyboard_interrupt
)
