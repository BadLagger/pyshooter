from pygame import *
from body import Body
import threading
import time
from bullet import Bullet
from keystorage import KeyStorage
from pprint import pprint

BODY_BORDER_COLOR = (200,15,25)
BODY_BULLET_COLOR = (20,150,25)

def draw_body(x1, y1, R):
    global sc
    draw.circle(sc, BODY_BORDER_COLOR, (y1, x1), R, 5)

def hide_body(x1, y1, R):
    global sc
    draw.circle(sc, (0,0,0), (y1, x1), R, 5)

def draw_line(x1, y1, x2, y2):
    global sc
    draw.line(sc, BODY_BORDER_COLOR, (y1, x1), (y2, x2), 5)

def hide_line(x1, y1, x2, y2):
    global sc
    draw.line(sc, (0,0,0), (y1, x1), (y2, x2), 5)

def shooter(x, y, mx, my):
    th = threading.Thread(target=shoot_th, args=(x,y,mx,my))
    th.start()

def shoot_th(x, y, mx, my):
    global sc
    bl = Bullet()
    bl.set_len(8)
    bl.set_bgn_point(x, y)
    bl.set_end_point(mx, my)
    while bl.get_next_pos() != None:
        b_line = bl.get_last_pos()
        draw.line(sc, BODY_BULLET_COLOR, b_line[0], b_line[1], 5)
        display.update()
        time.sleep(0.01)
        draw.line(sc, (0,0,0), b_line[0], b_line[1], 5)
        display.update()


class Display:
    def __init__(self, width, heigh):
        self.__size = (width, heigh)
        self.__bg = (0,0,0)
        self.__sc = display.set_mode((width, heigh))

    def set_bg(self, rgb):
        self.__bg = rgb
        self.__sc.fill(self.__bg)

    def get_bg(self):
        return self.__bg

    def draw_circle(self, coord, radius, color, border):
        draw.circle(self.__sc, color, coord, radius, border)
        display.update()

    def hide_circle(self, coord, radius, border):
        draw.circle(self.__sc, self.__bg, coord, radius, border)
        display.update()

    def draw_line(self, coor_bgn, coor_end, color, bold):
        draw.line(self.__sc, color, coor_bgn, coor_end, bold)
        display.update()

    def hide_line(self, coor_bgn, coor_end, bold):
        draw.line(self.__sc, self.__bg, coor_bgn, coor_end, bold)
        display.update()

    def get_size(self):
        return self.__size

    def shooter(self, x, y, mx, my):
        th = threading.Thread(target=self.__shoot_th, args=(x,y,mx,my))
        th.start()

    def __shoot_th(self, x, y, mx, my):
        bl = Bullet()
        bl.set_len(8)
        bl.set_bgn_point(x, y)
        bl.set_end_point(mx, my)
        while bl.get_next_pos() != None:
            b_line = bl.get_last_pos()
            self.draw_line(b_line[0], b_line[1], BODY_BULLET_COLOR, 5)
            #draw.line(sc, BODY_BULLET_COLOR, b_line[0], b_line[1], 5)
            #display.update()
            time.sleep(0.01)
            self.hide_line(b_line[0], b_line[1], 5)
            #draw.line(sc, (0,0,0), b_line[0], b_line[1], 5)
            #display.update()

# Main Body
disp = Display(1024, 600)

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
        #else:
        #    pass
    time.sleep(0.005)
