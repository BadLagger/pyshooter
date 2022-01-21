from pygame import *
from pygame import time as pgtime
import time
from body import Body
from body import BulletCollisionProperty
from body import BulletFlyProperty
from body import BodyLifeProperty
from bullet import Bullet
from keystorage import KeyStorage
from display import Display
from pprint import pprint
import threading


def fps_draw(esc):
    global fps_last
    global disp
    while(esc() == False):
        try:
            disp.show_text("FPS: %s" % int(fps_last))
        except:
            print('Silent except')
        time.sleep(1)

BODY_BORDER_COLOR = (0,0,0)
BODY_BUL_CLR = (200, 200, 0)
DISPLAY_BG_COLOR = (100, 100, 100)

# Main Body
disp = Display(1024, 600)
disp.set_bg(DISPLAY_BG_COLOR)

obj = Body(25, disp.get_size(), BODY_BORDER_COLOR, 2)
stuff = Body(30, disp.get_size(), BODY_BORDER_COLOR, 4)
stuff_2 = Body(30, disp.get_size(), BODY_BORDER_COLOR, 4)
disp.add_obj(stuff)
disp.add_obj(stuff_2)
key_bindings = {
    K_UP: {"object": obj, "handler": disp.mover_up},
    K_DOWN: {"object": obj, "handler": disp.mover_down},
    K_LEFT: {"object": obj, "handler": disp.mover_left},
    K_RIGHT: {"object": obj, "handler": disp.mover_right},
}
ks = KeyStorage(key_bindings)
obj.set_draw(disp.draw_circle)
obj.set_hide(disp.hide_circle)
obj.set_draw_line(disp.draw_line)
obj.set_hide_line(disp.hide_line)
obj.set_shooter(disp.shooter)
obj.set_bullet_prm(4, 3, BODY_BUL_CLR)
obj.set_bullet_fly(BulletFlyProperty.TILL_SCREEN)
obj.show()

stuff.set_draw(disp.draw_circle)
stuff.set_hide(disp.hide_circle)
stuff.set_pos(150, 150)
stuff.set_life(BodyLifeProperty.MORTAL)
stuff.show()

stuff_2.set_draw(disp.draw_circle)
stuff_2.set_hide(disp.hide_circle)
stuff_2.set_pos(400, 150)
stuff_2.set_bullet_collision(BulletCollisionProperty.STOP)
stuff_2.set_life(BodyLifeProperty.MORTAL, 3)
stuff_2.show()

clk = pgtime.Clock()
fps_last = 0
fps_draw_th = threading.Thread(target=fps_draw, args=(ks.get_esc,))
fps_draw_th.start()

while 1:
    for ev in event.get():
        if ev.type == QUIT:
            ks.shutdown()
            exit()
        elif ev.type == KEYDOWN:
            ks.add_key(ev.key)
        elif ev.type == KEYUP:
            ks.remove_key(ev.key)
        elif ev.type == MOUSEMOTION:
            obj.rotate(mouse.get_pos())
        elif ev.type == MOUSEBUTTONDOWN:
            ms = mouse.get_pos()
            obj.shoot(ms[0], ms[1])

    #stuff.update()
    #stuff_2.update()
    #    disp.show_text("FPS: %s" % int(fps_last))
    #    count = 0
    #else:
    #    count += 1
    #time.sleep(0.005)
    time.sleep(0.0001)
    clk.tick()
    fps_last = clk.get_fps()
