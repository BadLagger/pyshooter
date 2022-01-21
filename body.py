from enum import Enum

BODY_COUNTER = 0

class BulletCollisionProperty(Enum):
    TRANSPARENT = 1
    STOP = 2

class BulletFlyProperty(Enum):
    TILL_MOUSE  = 1
    TILL_SCREEN = 2

class BodyLifeProperty(Enum):
    IMMORTAL = 1
    MORTAL = 2

class Body:
    def __init__(self, radius, size, color, border_size, name=None):
        global BODY_COUNTER
        BODY_COUNTER += 1
        self.__name = name if name != None else ("Body%d" % BODY_COUNTER)
        self.__R  = radius
        self.__color = color
        self.__br_size = border_size
        self.__x1 = size[0] / 2
        self.__y1 = size[1] / 2
        self.__max_x = size[0]
        self.__max_y = size[1]
        self.__x2 = 0
        self.__y2 = 0
        self.__step = 1
        self.__visible = False
        self.__draw = None
        self.__hide = None
        self.__draw_line = None
        self.__hide_line = None
        self.__shooter = None
        self.__backward = None
        self.__last_ms_coord = None
        self.__bul_col_prop = BulletCollisionProperty.TRANSPARENT
        self.__bul_fly_prop = BulletFlyProperty.TILL_MOUSE
        self.__life_prop  = BodyLifeProperty.IMMORTAL
        self.__life_level = 0
        self.calc_x2_pos(self.__x2, self.__y2)

    #def __del__(self):
    #    global BODY_COUNTER
    #    print('Delete %s' % self.__name)
    #    BODY_COUNTER -= 1

    #def should_kill(self):
    #    return self.__kill

    def set_life(self, life_prop, life_lvl=0):
        if life_prop in BodyLifeProperty:
            self.__life_prop = life_prop
            self.__life_level = life_lvl
        else:
            raise ValueError('Bad BodyLifeProperty')

    def get_life_property(self):
        return self.__life_prop

    def get_life_level(self):
        return self.__life_level

    # if return False - than life lvl <= 0
    def make_damage(self, dmg_lvl = 1):
        if self.__life_prop == BodyLifeProperty.MORTAL:
            self.__life_level -= dmg_lvl
            if self.__life_level <= 0:
                return False
        return True

    def set_bullet_fly(self, prop):
        if prop in BulletFlyProperty:
            self.__bul_fly_prop = prop
        else:
            raise ValueError('Bad BulletFlyProperty')

    def get_bullet_fly(self):
        return self.__bul_fly_prop

    def set_bullet_collision(self, prop):
        if prop in BulletCollisionProperty:
            self.__bul_col_prop = prop
        else:
            raise ValueError('Bad BulletCollisionProperty')

    def get_bullet_collision(self):
        return self.__bul_col_prop

    def set_pos(self, x, y):
        self.__x1 = x
        self.__y1 = y

    def set_bullet_prm(self, len, width, color):
        self.bul_len = len
        self.bul_width = width
        self.bul_color = color

    def set_shooter(self, shooter):
        self.__shooter = shooter

    def set_draw(self, draw):
        self.__draw = draw

    def set_hide(self, hide):
        self.__hide = hide

    def set_draw_line(self, draw_line):
        self.__draw_line = draw_line

    def set_hide_line(self, hide_line):
        self.__hide_line = hide_line

    def isvisible(self):
        return self.__visible

    def show(self):
        if self.__draw:
            if self.__R:
                if not self.__visible:
                    self.__visible = True
                    self.__draw((self.__x1, self.__y1), self.__R, self.__color, self.__br_size)
                    if self.__draw_line:
                        self.__draw_line((self.__x1, self.__y1), (self.__x2, self.__y2), self.__color, self.__br_size)

    def hide(self):
        if self.__hide:
            if self.__visible:
                self.__visible = False
                self.__hide((self.__x1, self.__y1), self.__R, self.__br_size)
                if self.__hide_line:
                    self.__hide_line((self.__x1, self.__y1), (self.__x2, self.__y2), self.__br_size)

    def update(self):
        self.hide()
        self.show()

    def rotate(self, coord):
        if self.__draw_line and self.__hide_line and self.__visible:
            self.hide()
            self.__last_ms_coord = coord
            self.calc_x2_pos(coord[0], coord[1])
            self.show()

    def move_up(self, show_now=True):
        if self.__draw_line and self.__hide_line:
            if (self.__y1 - self.__step - self.__R) > 0:
                self.hide()
                self.__y1 -= self.__step
                self.__y2 -= self.__step
                if self.__draw_line:
                    self.calc_x2_pos(self.__last_ms_coord[0], self.__last_ms_coord[1])
                if show_now:
                    self.show()
                self.__backward = self.move_down
            return (self.__x1, self.__y1, self.__R)

    def move_down(self, show_now=True):
        if self.__draw_line and self.__hide_line:
            if (self.__y1 + self.__step + self.__R) < self.__max_y:
                self.hide()
                self.__y1 += self.__step
                self.__y2 += self.__step
                if self.__draw_line:
                    self.calc_x2_pos(self.__last_ms_coord[0], self.__last_ms_coord[1])
                if show_now:
                    self.show()
                self.__backward = self.move_up
            return (self.__x1, self.__y1, self.__R)

    def move_right(self, show_now=True):
        if self.__draw_line and self.__hide_line:
            if (self.__x1 + self.__step + self.__R) < self.__max_x:
                self.hide()
                self.__x1 += self.__step
                self.__x2 += self.__step
                if self.__draw_line:
                    self.calc_x2_pos(self.__last_ms_coord[0], self.__last_ms_coord[1])
                if show_now:
                    self.show()
                self.__backward = self.move_left
            return (self.__x1, self.__y1, self.__R)

    def move_left(self, show_now=True):
        if self.__draw_line and self.__hide_line:
            if (self.__x1 - self.__step - self.__R) > 0:
                self.hide()
                self.__x1 -= self.__step
                self.__x2 -= self.__step
                if self.__draw_line:
                    self.calc_x2_pos(self.__last_ms_coord[0], self.__last_ms_coord[1])
                if show_now:
                    self.show()
                self.__backward = self.move_right
            return (self.__x1, self.__y1, self.__R)

    def move_back(self, show_now=True):
        if self.__backward:
            self.__backward(show_now)

    def shoot(self, mx, my):
        if self.__shooter and self.__visible:
            if self.__bul_fly_prop == BulletFlyProperty.TILL_MOUSE:
                self.__shooter(self.__y2, self.__x2, my, mx, self.bul_len, self.bul_width, self.bul_color)
            elif self.__bul_fly_prop == BulletFlyProperty.TILL_SCREEN:
                a = {'x': mx - self.__x2, 'y': my - self.__y2}
                if a['x'] == 0:
                    my = 0 if my < self.__y2 else self.__max_y
                elif a['y'] == 0:
                    mx = 0 if mx < self.__x2 else self.__max_x
                else:
                    if a['y'] < 0:
                        x = self.__line_equation(a['x'], a['y'], 0, self.__y2, self.__x2)
                        if a['x'] < 0:
                            mx, my = (x, 0) if x > 0 else (0, self.__line_equation(a['y'], a['x'], 0, self.__x2, self.__y2))
                        else:                  #elif a['x'] > 0:
                            mx, my = (x, 0) if x < self.__max_x else (self.__max_x, self.__line_equation(a['y'], a['x'], self.__max_x, self.__x2, self.__y2))
                    else:                      #elif a['y'] > 0:
                        x = self.__line_equation(a['x'], a['y'], self.__max_y, self.__y2, self.__x2)
                        if a['x'] < 0:
                            mx, my = (x, self.__max_y) if x > 0 else (0, self.__line_equation(a['y'], a['x'], 0, self.__x2, self.__y2))
                        else:                  #elif a['x'] > 0:
                            mx, my = (x, self.__max_y) if x < self.__max_x else (self.__max_x, self.__line_equation(a['y'], a['x'], self.__max_x, self.__x2, self.__y2))
                self.__shooter(self.__y2, self.__x2, my, mx, self.bul_len, self.bul_width, self.bul_color)

    # If need to find y than:
    #  a1 = ay, a2 = ax, c1 = x, c2 = x0, c3 = y0
    def __line_equation(self, a1, a2, c1, c2, c3):
        return (a1 / a2) * (c1 - c2) + c3

    def point_belongs(self, coor):
        x = coor[0]
        y = coor[1]
        l = ((x - self.__x1) ** 2 + (y - self.__y1) ** 2 ) ** 0.5
        if l <= self.__R:
            return True
        return False

    def belongs(self, x1, y1, x2, y2, xp, yp):
        if xp >= x1 and xp <= x2 and yp >= y1 and yp <= y2:
            return True
        return False

    def collision(self, x, y, R):
        L = ((self.__x1 - x) ** 2 + (self.__y1 - y) ** 2) ** 0.5
        if L <= (self.__R + R):
            return True
        return False

    # Calculate point position of crossing circle line and mouse direction line
    def calc_x2_pos(self, x, y):
        if self.__x1 - x == 0:
            py = self.__R + self.__y1
            if self.belongs(self.__x1, self.__y1, x, y, self.__x1, py):
                self.__y2 = py
            else:
                self.__y2 = self.__y1 - self.__R
            self.__x2 = self.__x1
        elif self.__y1 - y == 0:
            px = self.__R + self.__x1
            if self.belongs(self.__x1, self.__y1, x, y, px, self.__y1):
                self.__x2 = px
            else:
                self.__x2 = self.__x1 - self.__R
            self.__y2 = self.__y1
        else:
            lamdax, lamday = self.lamda(x, y)
            self.__x2, self.__y2 = self.__x1 - lamdax, self.__y1 - lamday

    def lamda(self, x2, y2):
        ax = self.__x1 - x2
        ay = self.__y1 - y2
        retx = ((self.__R ** 2)/(((ay/ax) ** 2) + 1) ) ** 0.5
        rety = ((self.__R ** 2)/(((ax/ay) ** 2) + 1) ) ** 0.5
        if ax < 0:
            retx *= (-1)
        if ay < 0:
            rety *= (-1)
        return retx, rety
