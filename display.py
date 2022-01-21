from pygame import *
from bullet import Bullet
from body import BulletCollisionProperty
import threading
import time

class Display:
    def __init__(self, width, heigh):
        self.__size = (width, heigh)
        self.__bg = (0,0,0)
        self.__sc = display.set_mode((width, heigh))
        self.__ojects = []
        font.init()
        self.__fpsFont = font.SysFont('Comic Sans MS', 30)

    def show_text(self, text, pos=(0,0), color=(0,0,0)):
        draw.rect(self.__sc, self.__bg, (0,0, 200, 50))
        self.__sc.blit(self.__fpsFont.render(text, False, color), pos)

    def set_bg(self, rgb):
        self.__bg = rgb
        self.__sc.fill(self.__bg)
        display.update()

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

    def add_obj(self, obj):
        if obj in self.__ojects:
            raise ValueError("Try to register duplicate object")
        else:
            self.__ojects.append(obj)

    def mover_up(self, obj):
        self.__mover(obj, obj.move_up)

    def mover_down(self, obj):
        self.__mover(obj, obj.move_down)

    def mover_right(self, obj):
        self.__mover(obj, obj.move_right)

    def mover_left(self, obj):
        self.__mover(obj, obj.move_left)

    def __shoot_th(self, x, y, mx, my, bul_len, bul_width,bul_color):
        bl = Bullet()
        bl.set_len(bul_len)
        bl.set_bgn_point(x, y)
        bl.set_end_point(mx, my)
        while bl.get_next_pos() != None:
            bul_prop = BulletCollisionProperty.TRANSPARENT
            b_line = bl.get_last_pos()
            for obj in self.__ojects:
                if obj.point_belongs(b_line[0]) or obj.point_belongs(b_line[1]):
                    bul_prop = obj.get_bullet_collision()
                    if obj.make_damage() == False:
                        obj.hide()
                        self.__ojects.remove(obj)
                    break
                    #if bul_prop != BulletCollisionProperty.TRANSPARENT:
                    #    break
            if bul_prop == BulletCollisionProperty.STOP:
                bl.destroy()
            else:
                self.draw_line(b_line[0], b_line[1], bul_color, bul_width)
                time.sleep(0.01)
                self.hide_line(b_line[0], b_line[1], bul_width)

            #if dead_obj:
            #    self.__ojects.remove(dead_obj)
            #    del dead_obj
                #dead_obj.__del__()

    def __mover(self, obj, move):
        next_pos = move(False)
        for next_object in self.__ojects:
            if next_object.collision(next_pos[0], next_pos[1], next_pos[2]):
                obj.move_back(True)
                return
        obj.show()
