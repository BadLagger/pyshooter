from pygame import *
from bullet import Bullet
import threading
import time

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
        #display.update()

    def draw_line(self, coor_bgn, coor_end, color, bold):
        draw.line(self.__sc, color, coor_bgn, coor_end, bold)
        display.update()

    def hide_line(self, coor_bgn, coor_end, bold):
        draw.line(self.__sc, self.__bg, coor_bgn, coor_end, bold)
        #display.update()

    def get_size(self):
        return self.__size

    def shooter(self, x, y, mx, my, bul_len, bul_width, bul_color):
        th = threading.Thread(target=self.__shoot_th, args=(x,y,mx,my,bul_len,bul_width,bul_color))
        th.start()

    def __shoot_th(self, x, y, mx, my, bul_len, bul_width,bul_color):
        bl = Bullet()
        bl.set_len(bul_len)
        bl.set_bgn_point(x, y)
        bl.set_end_point(mx, my)
        while bl.get_next_pos() != None:
            b_line = bl.get_last_pos()
            self.draw_line(b_line[0], b_line[1], bul_color, bul_width)
            time.sleep(0.01)
            self.hide_line(b_line[0], b_line[1], bul_width)
