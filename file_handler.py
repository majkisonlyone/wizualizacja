from figures import *
from renderer import CameraOrientation


class FileReader:
    def __init__(self, file_name):
        self.file_name = file_name

    def read(self) -> tuple[list[Figure], CameraOrientation]:
        camera_params = CameraOrientation()
        objects = []
        with open(self.file_name, "r") as file:
            for line in file:
                splitted = line.split(" ")

                if splitted[0] == "Sphere":
                    x, y, z = splitted[1].split("xyz=")[1].split(",")
                    col = splitted[2].split("col=")[1]
                    angle_x, angle_y, angle_z = (
                        splitted[3].split("angle=")[1].split(",")
                    )
                    r, q = splitted[4].split("dim=")[1].split(",")
                    objects.append(
                        Sphere(
                            float(x),
                            float(y),
                            float(z),
                            col,
                            [float(angle_x), float(angle_y), float(angle_z)],
                        ).set_dimensions(float(r), int(q))
                    )

                if splitted[0] == "Cube":
                    x, y, z = splitted[1].split("xyz=")[1].split(",")
                    col = splitted[2].split("col=")[1].split(",")
                    angle_x, angle_y, angle_z = (
                        splitted[3].split("angle=")[1].split(",")
                    )
                    a = splitted[4].split("dim=")[1]
                    objects.append(
                        Cube(
                            float(x),
                            float(y),
                            float(z),
                            col,
                            [float(angle_x), float(angle_y), float(angle_z)],
                        ).set_dimensions(float(a), float(a), float(a))
                    )

                if splitted[0] == "Cylinder":
                    x, y, z = splitted[1].split("xyz=")[1].split(",")
                    col = splitted[2].split("col=")[1].split(",")
                    angle_x, angle_y, angle_z = (
                        splitted[3].split("angle=")[1].split(",")
                    )
                    r, h = splitted[4].split("dim=")[1].split(",")
                    objects.append(
                        Cylinder(
                            float(x),
                            float(y),
                            float(z),
                            col,
                            [float(angle_x), float(angle_y), float(angle_z)],
                        ).set_dimensions(float(r), float(h))
                    )

                if splitted[0] == "CameraOrientation":
                    dist = float(splitted[1])
                    angle_left_right = float(splitted[2])
                    angle_top_bottom = float(splitted[3])
                    camera_params = CameraOrientation(
                        dist, angle_left_right, angle_top_bottom
                    )

        return objects, camera_params


class FileWriter:
    def __init__(self):
        pass

### usage:
# reader = FileReader("file1.sci")
# reader.read()
