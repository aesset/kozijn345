class Stijl:
    def __init__(self, breedte, lengte):
        self.breedte = breedte
        self.lengte = lengte


class Dorpel:
    def __init__(self, hoogte, lengte):
        self.hoogte = hoogte
        self.lengte = lengte


class Kozijn:
    def __init__(self, bovendorpel: Dorpel, onderdorpel: Dorpel,
                 linkerstijl: Stijl, rechterstijl: Stijl):
        self.bovendorpel = bovendorpel
        self.onderdorpel = onderdorpel
        self.linkerstijl = linkerstijl
        self.rechterstijl = rechterstijl
        self.breedte = onderdorpel.lengte
        self.hoogte = linkerstijl.lengte + onderdorpel.hoogte + bovendorpel.hoogte


class Raam:
    def __init__(self, bovendorpel: Dorpel, onderdorpel: Dorpel,
                 linkerstijl: Stijl, rechterstijl: Stijl,
                 breedte_roedes: int, aantal_roedes_staand: int, aantal_roedes_liggend: int,
                 raampjes: list, roedes: list):
        self.bovendorpel = bovendorpel
        self.onderdorpel = onderdorpel
        self.linkerstijl = linkerstijl
        self.rechterstijl = rechterstijl
        self.breedte_roedes = breedte_roedes,
        self.aantal_roedes_staand = aantal_roedes_staand,
        self.aantal_roedes_liggend = aantal_roedes_liggend
        self.breedte = self.bovendorpel.lengte + self.linkerstijl.breedte + self.rechterstijl.breedte
        self.raampjes = raampjes
        self.roedes = roedes


class RaamKozijn:
    def __init__(self, kozijn: Kozijn, raam: Raam):
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
    def __init__(self, x, y, breedte, lengte, breedte_midden, pos, verstek_begin: bool, verstek_eind: bool):
        self.x = int(x)
        self.y = int(y)
        self.breedte = breedte
        self.lengte = int(lengte)
        self.breedte_midden = breedte_midden
        self.pos = pos
        self.verstek_begin = verstek_begin
        self.verstek_eind = verstek_eind

    def __str__(self):
        return f'Roede: {self.x},{self.y}, {self.breedte}x{self.lengte}x{self.breedte_midden} ' \
               f'pos={self.pos} verstek:{self.verstek_begin}/{self.verstek_eind}'


def create_roedes(aantal_raampjes_horizontaal,
                  aantal_raampjes_verticaal,
                  breedte_raampje,
                  hoogte_raampje,
                  breedte_roedes,
                  breedte_roedes_midden):
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
                roede = Roede(roede_x, roede_y, breedte_roedes, breedte_raampje, breedte_roedes_midden,
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
                roede = Roede(roede_x, roede_y, breedte_roedes, hoogte_raampje, breedte_roedes_midden,
                              positie, verstek_begin, verstek_eind)
                print(f'Roede: {roede}')
                roedes.append(roede)



    return roedes


def create_raam_kozijn(zicht_kozijn_stijlen: int,
                       zicht_kozijn_boven: int,
                       zicht_kozijn_onder: int,
                       zicht_raam_stijlen: int,
                       zicht_raam_boven: int,
                       zicht_raam_onder: int,
                       breedte_roedes: int,
                       breedte_roedes_midden: int,
                       aantal_roedes_staand: int,
                       aantal_roedes_liggend: int,
                       totaal_kozijn_breedte) -> RaamKozijn:
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

    kozijn_stijl_links = Stijl(zicht_kozijn_stijlen, kozijn_stijl_lengte)
    kozijn_stijl_rechts = Stijl(zicht_kozijn_stijlen, kozijn_stijl_lengte)

    kozijn_dorpel_onder = Dorpel(zicht_kozijn_boven, totaal_kozijn_breedte)
    kozijn_dorpel_boven = Dorpel(zicht_kozijn_onder, totaal_kozijn_breedte)

    kozijn = Kozijn(kozijn_dorpel_boven, kozijn_dorpel_onder, kozijn_stijl_links, kozijn_stijl_rechts)

    raam_stijl_lengte = kozijn_stijl_lengte

    raam_stijl_links = Stijl(zicht_raam_stijlen, raam_stijl_lengte)
    raam_stijl_rechts = Stijl(zicht_raam_stijlen, raam_stijl_lengte)

    raam_dorpel_lengte = breedte_raampje * aantal_raampjes_horizontaal \
                         + (breedte_roedes * aantal_roedes_staand)
    raam_dorpel_onder = Dorpel(zicht_raam_onder, raam_dorpel_lengte)
    raam_dorpel_boven = Dorpel(zicht_raam_boven, raam_dorpel_lengte)

    raampjes = create_raampjes(aantal_raampjes_horizontaal, aantal_raampjes_verticaal, breedte_raampje, hoogte_raampje,
                               breedte_roedes)

    roedes = create_roedes(aantal_raampjes_horizontaal, aantal_raampjes_verticaal, breedte_raampje, hoogte_raampje,
                           breedte_roedes, breedte_roedes_midden)

    raam = Raam(raam_dorpel_boven, raam_dorpel_onder, raam_stijl_links, raam_stijl_rechts,
                breedte_roedes, aantal_roedes_staand, aantal_roedes_liggend, raampjes, roedes)

    return RaamKozijn(kozijn, raam)
