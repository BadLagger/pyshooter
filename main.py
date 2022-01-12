from pygame import *
import time
from body import Body
from bullet import Bullet
from keystorage import KeyStorage
from display import Display
from pprint import pprint

BODY_BORDER_COLOR = (0,0,0)
BODY_BUL_CLR = (255, 255, 255)
DISPLAY_BG_COLOR = (100, 100, 100)

# Main Body
disp = Display(1024, 600)
disp.set_bg(DISPLAY_BG_COLOR)

obj = Body(25, disp.get_size(), BODY_BORDER_COLOR, 2)
key_bindings = {
    K_UP: obj.move_up,
    K_DOWN: obj.move_down,
    K_LEFT: obj.move_left,
    K_RIGHT: obj.move_right
}
ks = KeyStorage(key_bindings)
obj.set_draw(disp.draw_circle)
obj.set_hide(disp.hide_circle)
obj.set_draw_line(disp.draw_line)
obj.set_hide_line(disp.hide_line)
obj.set_shooter(disp.shooter)
obj.set_bullet_prm(4, 3, BODY_BUL_CLR)
obj.show()

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
            obj.shoot(ms[1], ms[0])
    time.sleep(0.005)
