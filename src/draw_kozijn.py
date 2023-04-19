from drawsvg import Lines
from drawsvg import Rectangle

from config import SCALE
from src.kozijn import Dorpel
from src.kozijn import Kozijn
from src.kozijn import Raam
from src.kozijn import Roede
from src.kozijn import Stijl


def create_rectangle_for_dorpel(x: int, y: int, dorpel: Dorpel) -> Rectangle:
    return Rectangle(x, y, dorpel.lengte, dorpel.hoogte,
                     fill='white', stroke='black', transform=f'scale({SCALE})')


def create_rectangle_for_stijl(x: int, y: int, stijl: Stijl) -> Rectangle:
    return Rectangle(x, y, stijl.breedte, stijl.lengte,
                     fill='white', stroke='black', transform=f'scale({SCALE})')


def draw_kozijn(d, kozijn: Kozijn):
    d.append(create_rectangle_for_dorpel(0, 0, kozijn.bovendorpel))
    d.append((create_rectangle_for_stijl(0, kozijn.bovendorpel.hoogte, kozijn.linkerstijl)))
    d.append(create_rectangle_for_dorpel(0, kozijn.onderdorpel.hoogte + kozijn.linkerstijl.lengte, kozijn.onderdorpel))
    d.append(
        (create_rectangle_for_stijl(kozijn.bovendorpel.lengte - kozijn.rechterstijl.breedte, kozijn.bovendorpel.hoogte,
                                    kozijn.rechterstijl)))


def draw_raam(d, x, y, raam: Raam):
    d.append(create_rectangle_for_dorpel(x + raam.linkerstijl.breedte, y, raam.bovendorpel))
    d.append(
        create_rectangle_for_dorpel(x + raam.linkerstijl.breedte, y + raam.linkerstijl.lengte - raam.onderdorpel.hoogte,
                                    raam.onderdorpel))
    d.append(create_rectangle_for_stijl(x, y, raam.linkerstijl))
    d.append(create_rectangle_for_stijl(x + raam.linkerstijl.breedte + raam.bovendorpel.lengte, y, raam.rechterstijl))

    raampjes_offset_x = x + raam.linkerstijl.breedte
    raampjes_offset_y = y + raam.bovendorpel.hoogte

    for raampje in raam.raampjes:
        d.append(Rectangle(raampjes_offset_x + raampje.x,
                           raampjes_offset_y + raampje.y,
                           raampje.breedte, raampje.hoogte, fill='#eef4f5', stroke='black',
                           transform=f'scale({SCALE})'))


class Coordinates:
    def __init__(self):
        self.x_points = []
        self.y_points = []
        self.prev_x = 0
        self.prev_y = 0

    def add(self, x, y):
        self.x_points.append(x)
        self.y_points.append(y)
        self.prev_x = x
        self.prev_y = y

    def move_y(self, shift):
        self.add(self.prev_x, self.prev_y + shift)
        return self.prev_x, self.prev_y

    def move(self, shift_x, shift_y):
        self.add(self.prev_x + shift_x, self.prev_y + shift_y)
        return self.prev_x, self.prev_y

    def set_without_memory(self, x, y):
        self.x_points.append(x)
        self.y_points.append(y)


def drawy_xy_as_line_on_d(d, coordinates: Coordinates):
    xy = [item for sublist in zip(coordinates.x_points, coordinates.y_points) for item in sublist]
    lines = Lines(*xy, stroke='black', stroke_width=1, fill='white', transform=f'scale({SCALE})')
    d.append(lines)


def draw_roedes(d, x, y, raam: Raam):
    linker_bovenhoek_raampjes_x = x + raam.linkerstijl.breedte
    linker_bovenhoek_raampjes_y = y + raam.bovendorpel.hoogte

    roede_randje = raam.roede_randje

    roede: Roede
    for roede in raam.roedes:
        coordinates = Coordinates()

        start_roede_x = linker_bovenhoek_raampjes_x + roede.x
        start_roede_y = linker_bovenhoek_raampjes_y + roede.y
        x = start_roede_x
        y = start_roede_y
        coordinates.add(x, y)

        if roede.pos == 'h':
            x, y = coordinates.move(roede.lengte, 0)

            if roede.verstek_eind:
                coordinates.set_without_memory(x + (roede.breedte / 2),
                                               y + (roede.breedte / 2))

            x, y = coordinates.move(0, roede.breedte)
            x, y = coordinates.move(-roede.lengte, 0)

            if roede.verstek_begin:
                coordinates.set_without_memory(x - (roede.breedte / 2),
                                               y - (roede.breedte / 2))

            x, y = coordinates.move(0, -roede.breedte)

        if roede.pos == 'v':
            x, y = coordinates.move(0, roede.lengte)

            if roede.verstek_eind:
                coordinates.set_without_memory(x + (roede.breedte / 2),
                                               y + (roede.breedte / 2))

            x, y = coordinates.move(roede.breedte, 0)
            x, y = coordinates.move(0, -roede.lengte)

            if roede.verstek_begin:
                coordinates.set_without_memory(x - (roede.breedte / 2),
                                               y - (roede.breedte / 2))

            x, y = coordinates.move(-roede.breedte, 0)

        drawy_xy_as_line_on_d(d, coordinates)

        if roede_randje > 0:

            if roede.pos == 'h':

                coordinates = Coordinates()

                if roede.verstek_begin:
                    x, y = coordinates.move(start_roede_x - roede_randje, start_roede_y + roede_randje)
                else:
                    x, y = coordinates.move(start_roede_x, start_roede_y + roede_randje)

                x = start_roede_x + roede.lengte
                if roede.verstek_eind:
                    x += roede_randje
                coordinates.add(x, y)

                drawy_xy_as_line_on_d(d, coordinates)

                coordinates = Coordinates()

                y = start_roede_y + roede.breedte - roede_randje
                coordinates.add(x, y)

                x = start_roede_x
                if roede.verstek_begin:
                    x -= roede_randje
                coordinates.add(x, y)

                drawy_xy_as_line_on_d(d, coordinates)

            if roede.pos == 'v':

                coordinates = Coordinates()

                x = start_roede_x + roede_randje
                y = start_roede_y
                if roede.verstek_begin:
                    y -= roede_randje
                coordinates.add(x, y)

                y = start_roede_y + roede.lengte
                if roede.verstek_eind:
                    y += roede_randje
                coordinates.add(x, y)

                drawy_xy_as_line_on_d(d, coordinates)

                coordinates = Coordinates()

                x = start_roede_x + roede.breedte - roede_randje
                coordinates.add(x, y)

                y = start_roede_y
                if roede.verstek_begin:
                    y -= roede_randje
                coordinates.add(x, y)

                drawy_xy_as_line_on_d(d, coordinates)
