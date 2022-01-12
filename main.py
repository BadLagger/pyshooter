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

def key_watch(args):
    while args["esc"] == False:
        args["call"]()
        time.sleep(0.1)

class KeyStorage:
    def __init__(self, key_bind):
        self.__key_array = []
        self.__key_th_arg = {}
        self.__key_th_arg["esc"] = False
        self.__key_th = threading.Thread(target=self.__thread, args=(self.__key_th_arg,))
        self.__key_th.start()
        self.__key_bind = key_bind

    def add_key(self, key):
        self.__key_array.append(key)
        self.__process(key)

    def remove_key(self, key):
        if self.__key_array.count(key) != 0:
            self.__key_array.remove(key)
    
    def shutdown(self):
        self.__key_th_arg["esc"] = True
        self.__key_th.join()

    def __check_keys(self):
        if len(self.__key_array):
            for key in self.__key_array:
                self.__process(key)
                
    def __thread(self, args):
        while args["esc"] == False:
            self.__check_keys()
            time.sleep(0.1)
    
    def __process(self, key):
        for k in self.__key_bind:
            if k == key:
                self.__key_bind[k]()
                break
            

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
    
    #def shooter(self, )

# Main Body
disp = Display(800, 600)

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
#obj.set_shooter(shooter)
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
        #elif ev.type == MOUSEBUTTONDOWN:
        #    ms = mouse.get_pos()
        #    obj.shoot(ms[1], ms[0])
        #else:
        #    pass
    time.sleep(0.005)
