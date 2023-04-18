from drawsvg import Lines
from drawsvg import Rectangle

from config import SCALE
from kozijn import Dorpel
from kozijn import Kozijn
from kozijn import Raam
from kozijn import Roede
from kozijn import Stijl


def rectangle_dorpel(x: int, y: int, dorpel: Dorpel) -> Rectangle:
    return Rectangle(x, y, dorpel.lengte, dorpel.hoogte,
                     fill='white', stroke='black', transform=f'scale({SCALE})')


def rectangle_stijl(x: int, y: int, stijl: Stijl) -> Rectangle:
    return Rectangle(x, y, stijl.breedte, stijl.lengte,
                     fill='white', stroke='black', transform=f'scale({SCALE})')


def draw_kozijn(d, kozijn: Kozijn):
    d.append(rectangle_dorpel(0, 0, kozijn.bovendorpel))
    d.append((rectangle_stijl(0, kozijn.bovendorpel.hoogte, kozijn.linkerstijl)))
    d.append(rectangle_dorpel(0, kozijn.onderdorpel.hoogte + kozijn.linkerstijl.lengte, kozijn.onderdorpel))
    d.append((rectangle_stijl(kozijn.bovendorpel.lengte - kozijn.rechterstijl.breedte, kozijn.bovendorpel.hoogte,
                              kozijn.rechterstijl)))


def draw_raam(d, x, y, raam: Raam):
    d.append(rectangle_dorpel(x + raam.linkerstijl.breedte, y, raam.bovendorpel))
    d.append(rectangle_dorpel(x + raam.linkerstijl.breedte, y + raam.linkerstijl.lengte - raam.onderdorpel.hoogte,
                              raam.onderdorpel))
    d.append(rectangle_stijl(x, y, raam.linkerstijl))
    d.append(rectangle_stijl(x + raam.linkerstijl.breedte + raam.bovendorpel.lengte, y, raam.rechterstijl))

    raampjes_offset_x = x + raam.linkerstijl.breedte
    raampjes_offset_y = y + raam.bovendorpel.hoogte

    for raampje in raam.raampjes:
        d.append(Rectangle(raampjes_offset_x + raampje.x,
                           raampjes_offset_y + raampje.y,
                           raampje.breedte, raampje.hoogte, fill='#eef4f5', stroke='black', transform=f'scale({SCALE})'))


def draw_roedes(d, x, y, raam: Raam):
    linker_bovenhoek_raampjes_x = x + raam.linkerstijl.breedte
    linker_bovenhoek_raampjes_y = y + raam.bovendorpel.hoogte

    roede: Roede
    for roede in raam.roedes:
        x_points = []
        y_points = []

        x = linker_bovenhoek_raampjes_x + roede.x
        y = linker_bovenhoek_raampjes_y + roede.y
        x_points.append(x)
        y_points.append(y)

        if roede.pos == 'h':
            x += roede.lengte
            x_points.append(x)
            y_points.append(y)
            if roede.verstek_eind:
                x_points.append(x + (roede.breedte / 2))
                y_points.append(y + (roede.breedte / 2))
            x_points.append(x)
            y += roede.breedte
            y_points.append(y)
            x -= roede.lengte
            x_points.append(x)
            y_points.append(y)
            if roede.verstek_begin:
                x_points.append(x - (roede.breedte / 2))
                y_points.append(y - (roede.breedte / 2))
            x_points.append(x)
            y -= roede.breedte
            y_points.append(y)

        if roede.pos == 'v':
            y += roede.lengte
            x_points.append(x)
            y_points.append(y)
            if roede.verstek_eind:
                x_points.append(x + (roede.breedte / 2))
                y_points.append(y + (roede.breedte / 2))

            x += roede.breedte
            x_points.append(x)
            y_points.append(y)

            y -= roede.lengte
            x_points.append(x)
            y_points.append(y)
            if roede.verstek_begin:
                x_points.append(x - (roede.breedte / 2))
                y_points.append(y - (roede.breedte / 2))
            x -= roede.breedte
            x_points.append(x)
            y_points.append(y)

        xy = [item for sublist in zip(x_points, y_points) for item in sublist]
        lines = Lines(*xy, stroke='black', stroke_width=1, fill='white', transform=f'scale({SCALE})')
        d.append(lines)
