from pygame import *
from body import Body
import threading
import time
from bullet import Bullet
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
    last_point_x, last_point_y = 0, 0
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

def key_bindings(key):
    global obj
    if key == K_ESCAPE:
        if obj.isvisible():
            obj.hide()
        else:
            obj.show()
    elif key == K_UP:
        obj.move_up()
    elif key == K_DOWN:
        obj.move_down()
    elif key == K_RIGHT:
        obj.move_right()
    elif key == K_LEFT:
        obj.move_left()

def key_process(key):
    key_bindings(key)
    display.update()

def key_watch(args):
    while args["esc"] == False:
        args["call"]()
        time.sleep(0.1)

class KeyStorage:
    def __init__(self, ext_handler):
        self.__key_array = []
        self.__callback = ext_handler

    def add_key(self, key):
        self.__key_array.append(key)

    def remove_key(self, key):
        if self.__key_array.count(key) != 0:
            self.__key_array.remove(key)

    def check_keys(self):
        if len(self.__key_array):
            for key in self.__key_array:
                self.__callback(key)

# Main Body
sc = display.set_mode((800, 600))
ks = KeyStorage(key_process)

obj = Body(300, 400, 50, 600, 800)
obj.set_draw(draw_body)
obj.set_hide(hide_body)
obj.set_draw_line(draw_line)
obj.set_hide_line(hide_line)
obj.set_shooter(shooter)
obj.show()

display.update()
th_args = {}
th_args["esc"] = False
th_args["call"] = ks.check_keys
th = threading.Thread(target=key_watch, args=(th_args,))
th.start()

while 1:
    for ev in event.get():
        if ev.type == QUIT:
            th_args["esc"] = True
            th.join()
            exit()
        elif ev.type == KEYDOWN:
            ks.add_key(ev.key)
            key_process(ev.key)
        elif ev.type == KEYUP:
            #print('key up: ', ev.key)
            ks.remove_key(ev.key)
        elif ev.type == MOUSEMOTION:
            ms = mouse.get_pos()
            obj.rotate(ms[1], ms[0])
            display.update()
        elif ev.type == MOUSEBUTTONDOWN:
            ms = mouse.get_pos()
            obj.shoot(ms[1], ms[0])
        else:
            pass
    time.sleep(0.005)
    #time.delay(100)
