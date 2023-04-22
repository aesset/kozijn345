from drawsvg import Drawing

from config import SCALE
from src.kozijn import create_raam_kozijn

zicht_kozijn_stijlen = 68
zicht_kozijn_boven = 68
zicht_kozijn_onder = 68

zicht_raam_stijlen = 75
zicht_raam_boven = 75
zicht_raam_onder = 85

breedte_roedes = 21
roede_randje = 4
aantal_roedes_staand = 1
aantal_roedes_liggend = 2

kozijn_breedte = 750

raam_kozijn = create_raam_kozijn(zicht_kozijn_stijlen, zicht_kozijn_boven, zicht_kozijn_onder,
                                 zicht_raam_stijlen, zicht_raam_boven, zicht_raam_onder,
                                 breedte_roedes, roede_randje,
                                 aantal_roedes_staand, aantal_roedes_liggend,
                                 kozijn_breedte)

canvas_marge = 10
breedte_canvas = (raam_kozijn.breedte * SCALE) + canvas_marge
hoogte_canvas = (raam_kozijn.hoogte * SCALE) + canvas_marge

d = Drawing(breedte_canvas, hoogte_canvas, origin=(-canvas_marge/2, -canvas_marge/2))

kozijn = raam_kozijn.kozijn
raam = raam_kozijn.raam

kozijn.draw(d, 0, 0)

raam_start_x = kozijn.linkerstijl.breedte
raam_start_y = kozijn.bovendorpel.hoogte
raam.draw(d, raam_start_x, raam_start_y)

raam.draw_roedes(d, raam_start_x, raam_start_y)

d.save_svg('output/kozijn.svg')
d.save_html('output/kozijn.html')
d.save_png('output/kozijn.png')
