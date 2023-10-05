from src.model import RaamKozijn


def test_create_kozijn():
    zicht_kozijn_stijlen = 10
    zicht_kozijn_boven = 10
    zicht_kozijn_onder = 10

    zicht_raam_stijlen = 10
    zicht_raam_boven = 10
    zicht_raam_onder = 10

    breedte_roedes = 10
    breedte_roedes_midden = 18  # doet ie nog niets mee
    aantal_roedes_staand = 1
    aantal_roedes_liggend = 1

    kozijn_breedte = 110

    raam_kozijn = RaamKozijn(zicht_kozijn_stijlen, zicht_kozijn_boven, zicht_kozijn_onder,
                             zicht_raam_stijlen, zicht_raam_boven, zicht_raam_onder,
                             breedte_roedes, breedte_roedes_midden,
                             aantal_roedes_staand, aantal_roedes_liggend,
                             kozijn_breedte, roede_latje_dikte=2)

    assert raam_kozijn.kozijn.bovendorpel.lengte == kozijn_breedte
    assert raam_kozijn.kozijn.hoogte == 130
    assert len(raam_kozijn.raam.raampjes) == 4
    assert raam_kozijn.raam.raampjes[0].hoogte == 40
