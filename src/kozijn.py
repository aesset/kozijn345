from drawsvg import Lines
from drawsvg import Rectangle
from drawsvg import Rectangle
from drawsvg import Rectangle
from drawsvg import Rectangle
from drawsvg import Rectangle

from config import SCALE
from config import SCALE
from config import SCALE
from config import SCALE


class Stijl:
    def __init__(self, breedte, lengte):
        self.breedte = breedte
        self.lengte = lengte

    def draw(self, d, x, y):
        d.append((create_rectangle_for_stijl(x, y, self)))


class Dorpel:
    def __init__(self, hoogte, lengte):
        self.hoogte = hoogte
        self.lengte = lengte

    def draw(self, d, x, y):
        d.append(create_rectangle_for_dorpel(x, y, self))


class Kozijn:
    def __init__(self, zicht_kozijn_stijlen, kozijn_stijl_lengte,
                 zicht_kozijn_boven, zicht_kozijn_onder, totaal_kozijn_breedte):

        self.linkerstijl = Stijl(zicht_kozijn_stijlen, kozijn_stijl_lengte)
        self.rechterstijl = Stijl(zicht_kozijn_stijlen, kozijn_stijl_lengte)

        self.onderdorpel = Dorpel(zicht_kozijn_boven, totaal_kozijn_breedte)
        self.bovendorpel = Dorpel(zicht_kozijn_onder, totaal_kozijn_breedte)

        self.breedte = self.onderdorpel.lengte
        self.hoogte = self.linkerstijl.lengte + self.onderdorpel.hoogte + self.bovendorpel.hoogte

    def draw(self, d, x, y):
        self.bovendorpel.draw(d, x, y)
        self.linkerstijl.draw(d, x, y + self.bovendorpel.hoogte)
        self.onderdorpel.draw(d, x, y + self.onderdorpel.hoogte + self.linkerstijl.lengte)
        self.rechterstijl.draw(d, x + self.bovendorpel.lengte - self.rechterstijl.breedte,
                               y + self.bovendorpel.hoogte)


class Raam:
    def __init__(self, bovendorpel: Dorpel, onderdorpel: Dorpel, linkerstijl: Stijl, rechterstijl: Stijl,
                 breedte_roedes: int, aantal_roedes_staand: int, aantal_roedes_liggend: int, raampjes: list,
                 roedes: list):
        self.bovendorpel = bovendorpel
        self.onderdorpel = onderdorpel
        self.linkerstijl = linkerstijl
        self.rechterstijl = rechterstijl
        self.breedte_roedes = breedte_roedes
        self.aantal_roedes_staand = aantal_roedes_staand
        self.aantal_roedes_liggend = aantal_roedes_liggend
        self.breedte = self.bovendorpel.lengte + self.linkerstijl.breedte + self.rechterstijl.breedte
        self.raampjes = raampjes
        self.roedes = roedes

    def draw(self, d, x, y):
        d.append(create_rectangle_for_dorpel(x + self.linkerstijl.breedte, y, self.bovendorpel))
        d.append(
            create_rectangle_for_dorpel(x + self.linkerstijl.breedte,
                                        y + self.linkerstijl.lengte - self.onderdorpel.hoogte,
                                        self.onderdorpel))
        d.append(create_rectangle_for_stijl(x, y, self.linkerstijl))
        d.append(
            create_rectangle_for_stijl(x + self.linkerstijl.breedte + self.bovendorpel.lengte, y, self.rechterstijl))

        raampjes_offset_x = x + self.linkerstijl.breedte
        raampjes_offset_y = y + self.bovendorpel.hoogte

        for raampje in self.raampjes:
            d.append(Rectangle(raampjes_offset_x + raampje.x,
                               raampjes_offset_y + raampje.y,
                               raampje.breedte, raampje.hoogte, fill='#eef4f5', stroke='black',
                               transform=f'scale({SCALE})'))

    def draw_roedes(self, d, x, y):
        linker_bovenhoek_raampjes_x = x + self.linkerstijl.breedte
        linker_bovenhoek_raampjes_y = y + self.bovendorpel.hoogte

        roede: Roede
        for roede in self.roedes:
            start_roede_x = linker_bovenhoek_raampjes_x + roede.x
            start_roede_y = linker_bovenhoek_raampjes_y + roede.y

            roede.draw(d, start_roede_x, start_roede_y)


class RaamKozijn:
    def __init__(self, zicht_kozijn_stijlen: int,
                 zicht_kozijn_boven: int,
                 zicht_kozijn_onder: int,
                 zicht_raam_stijlen: int,
                 zicht_raam_boven: int,
                 zicht_raam_onder: int,
                 breedte_roedes: int,
                 roede_randje: int,
                 aantal_roedes_staand: int,
                 aantal_roedes_liggend: int,
                 totaal_kozijn_breedte):

        zicht_kozijn_plus_raam_breedte = zicht_kozijn_stijlen + zicht_raam_stijlen
        totaal_zicht_kozijn_plus_raam_breedte = zicht_kozijn_plus_raam_breedte * 2

        zicht_kozijn_raam_boven = zicht_kozijn_boven + zicht_raam_boven
        zicht_kozijn_raam_onder = zicht_kozijn_onder + zicht_raam_onder
        totaal_zicht_kozijn_plus_raam_hoogte = zicht_kozijn_raam_boven + zicht_kozijn_raam_onder

        aantal_raampjes_horizontaal = aantal_roedes_staand + 1
        aantal_raampjes_verticaal = aantal_roedes_liggend + 1

        breedte_raampje = (totaal_kozijn_breedte
                           - totaal_zicht_kozijn_plus_raam_breedte
                           - (aantal_roedes_staand * breedte_roedes)) / aantal_raampjes_horizontaal

        hoogte_raampje = (breedte_raampje / 3) * 4

        kozijn_stijl_lengte = (hoogte_raampje * aantal_raampjes_verticaal) \
                              + (aantal_roedes_liggend * breedte_roedes) \
                              + zicht_raam_boven + zicht_raam_onder

        totaal_hoogte_kozijn = kozijn_stijl_lengte + totaal_zicht_kozijn_plus_raam_hoogte

        kozijn = Kozijn(zicht_kozijn_stijlen, kozijn_stijl_lengte, zicht_kozijn_boven, zicht_kozijn_onder, totaal_kozijn_breedte)

        raam_stijl_lengte = kozijn_stijl_lengte

        raam_stijl_links = Stijl(zicht_raam_stijlen, raam_stijl_lengte)
        raam_stijl_rechts = Stijl(zicht_raam_stijlen, raam_stijl_lengte)

        raam_dorpel_lengte = breedte_raampje * aantal_raampjes_horizontaal \
                             + (breedte_roedes * aantal_roedes_staand)
        raam_dorpel_onder = Dorpel(zicht_raam_onder, raam_dorpel_lengte)
        raam_dorpel_boven = Dorpel(zicht_raam_boven, raam_dorpel_lengte)

        raampjes = create_raampjes(aantal_raampjes_horizontaal, aantal_raampjes_verticaal, breedte_raampje,
                                   hoogte_raampje,
                                   breedte_roedes)

        roedes = create_roedes(aantal_raampjes_horizontaal, aantal_raampjes_verticaal, breedte_raampje, hoogte_raampje,
                               breedte_roedes, roede_randje)

        raam = Raam(raam_dorpel_boven, raam_dorpel_onder, raam_stijl_links, raam_stijl_rechts, breedte_roedes,
                    aantal_roedes_staand, aantal_roedes_liggend, raampjes, roedes)

        self.kozijn = kozijn
        self.raam = raam
        self.breedte = kozijn.breedte
        self.hoogte = kozijn.hoogte


class Raampje:
    def __init__(self, x, y, breedte, hoogte):
        self.x = x
        self.y = y
        self.breedte = breedte
        self.hoogte = hoogte


def create_raampjes(aantal_raampjes_horizontaal, aantal_raampjes_verticaal, breedte_raampje, hoogte_raampje,
                    breedte_roedes) -> list:
    raampjes = []

    for x in range(aantal_raampjes_horizontaal):
        for y in range(aantal_raampjes_verticaal):
            origin_x = x * (breedte_raampje + breedte_roedes)
            origin_y = y * (hoogte_raampje + breedte_roedes)
            raampje = Raampje(origin_x, origin_y, breedte_raampje, hoogte_raampje)
            raampjes.append(raampje)

    return raampjes


class Roede:
    def __init__(self, x, y, breedte, lengte, roede_randje, pos, verstek_begin: bool, verstek_eind: bool):
        self.x = int(x)
        self.y = int(y)
        self.breedte = breedte
        self.lengte = int(lengte)
        self.roede_randje = roede_randje
        self.pos = pos
        self.verstek_begin = verstek_begin
        self.verstek_eind = verstek_eind

    def __str__(self):
        return f'Roede: {self.x},{self.y}, {self.breedte}x{self.lengte}x{self.roede_randje} ' \
               f'pos={self.pos} verstek:{self.verstek_begin}/{self.verstek_eind}'

    def draw(self, d, start_roede_x, start_roede_y):
        x = start_roede_x
        y = start_roede_y

        coordinates = Coordinates()
        coordinates.add(x, y)

        if self.pos == 'h':
            x, y = coordinates.move(self.lengte, 0)

            if self.verstek_eind:
                coordinates.set_without_memory(x + (self.breedte / 2),
                                               y + (self.breedte / 2))

            x, y = coordinates.move(0, self.breedte)
            x, y = coordinates.move(-self.lengte, 0)

            if self.verstek_begin:
                coordinates.set_without_memory(x - (self.breedte / 2),
                                               y - (self.breedte / 2))

            x, y = coordinates.move(0, -self.breedte)

        if self.pos == 'v':
            x, y = coordinates.move(0, self.lengte)

            if self.verstek_eind:
                coordinates.set_without_memory(x + (self.breedte / 2),
                                               y + (self.breedte / 2))

            x, y = coordinates.move(self.breedte, 0)
            x, y = coordinates.move(0, -self.lengte)

            if self.verstek_begin:
                coordinates.set_without_memory(x - (self.breedte / 2),
                                               y - (self.breedte / 2))

            x, y = coordinates.move(-self.breedte, 0)

        drawy_xy_as_line_on_d(d, coordinates)

        if self.roede_randje > 0:

            if self.pos == 'h':

                coordinates = Coordinates()

                if self.verstek_begin:
                    x, y = coordinates.move(start_roede_x - self.roede_randje, start_roede_y + self.roede_randje)
                else:
                    x, y = coordinates.move(start_roede_x, start_roede_y + self.roede_randje)

                x = start_roede_x + self.lengte
                if self.verstek_eind:
                    x += self.roede_randje
                coordinates.add(x, y)

                drawy_xy_as_line_on_d(d, coordinates)

                coordinates = Coordinates()

                y = start_roede_y + self.breedte - self.roede_randje
                coordinates.add(x, y)

                x = start_roede_x
                if self.verstek_begin:
                    x -= self.roede_randje
                coordinates.add(x, y)

                drawy_xy_as_line_on_d(d, coordinates)

            if self.pos == 'v':

                coordinates = Coordinates()

                x = start_roede_x + self.roede_randje
                y = start_roede_y
                if self.verstek_begin:
                    y -= self.roede_randje
                coordinates.add(x, y)

                y = start_roede_y + self.lengte
                if self.verstek_eind:
                    y += self.roede_randje
                coordinates.add(x, y)

                drawy_xy_as_line_on_d(d, coordinates)

                coordinates = Coordinates()

                x = start_roede_x + self.breedte - self.roede_randje
                coordinates.add(x, y)

                y = start_roede_y
                if self.verstek_begin:
                    y -= self.roede_randje
                coordinates.add(x, y)

                drawy_xy_as_line_on_d(d, coordinates)


def create_roedes(aantal_raampjes_horizontaal,
                  aantal_raampjes_verticaal,
                  breedte_raampje,
                  hoogte_raampje,
                  breedte_roedes,
                  roede_randje):
    roedes = []

    for x in range(aantal_raampjes_horizontaal):
        for y in range(aantal_raampjes_verticaal):
            if not y == aantal_raampjes_verticaal - 1:

                positie = 'h'
                roede_x = ((x + 0) * breedte_raampje) + (x * breedte_roedes)
                roede_y = ((y + 1) * hoogte_raampje) + (y * breedte_roedes)
                verstek_begin = True
                verstek_eind = True
                if x == 0:
                    verstek_begin = False
                if x == aantal_raampjes_horizontaal - 1:
                    verstek_eind = False
                roede = Roede(roede_x, roede_y, breedte_roedes, breedte_raampje, roede_randje,
                              positie, verstek_begin, verstek_eind)
                print(f'Roede: {roede}')
                roedes.append(roede)

            if not x == aantal_raampjes_horizontaal - 1:
                positie = 'v'
                roede_x = ((x + 1) * breedte_raampje) + (x * breedte_roedes)
                roede_y = ((y + 0) * hoogte_raampje) + (y * breedte_roedes)
                verstek_begin = True
                verstek_eind = True
                if y == 0:
                    verstek_begin = False
                if y == aantal_raampjes_verticaal - 1:
                    verstek_eind = False
                roede = Roede(roede_x, roede_y, breedte_roedes, hoogte_raampje, roede_randje,
                              positie, verstek_begin, verstek_eind)
                print(f'Roede: {roede}')
                roedes.append(roede)

    return roedes


def create_rectangle_for_dorpel(x: int, y: int, dorpel: Dorpel) -> Rectangle:
    return Rectangle(x, y, dorpel.lengte, dorpel.hoogte,
                     fill='white', stroke='black', transform=f'scale({SCALE})')


def create_rectangle_for_stijl(x: int, y: int, stijl: Stijl) -> Rectangle:
    return Rectangle(x, y, stijl.breedte, stijl.lengte,
                     fill='white', stroke='black', transform=f'scale({SCALE})')


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
