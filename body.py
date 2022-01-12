class Body:
    def __init__(self, radius, size, color, border_size):
        self.__R  = radius
        self.__color = color
        self.__br_size = border_size
        self.__x1 = size[0] / 2
        self.__y1 = size[1] / 2
        self.__max_x = size[0]
        self.__max_y = size[1]
        self.__x2 = 0
        self.__y2 = 0
        self.__step = 10
        self.__visible = False
        self.__draw = None
        self.__hide = None
        self.__draw_line = None
        self.__hide_line = None
        self.__shooter = None
        self.calc_x2_pos(self.__x2, self.__y2)


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
        if self.__draw and self.__draw_line:
            if self.__R:
                if not self.__visible:
                    self.__visible = True
                    self.__draw((self.__x1, self.__y1), self.__R, self.__color, self.__br_size)
                    self.__draw_line((self.__x1, self.__y1), (self.__x2, self.__y2), self.__color, self.__br_size)

    def hide(self):
        if self.__hide and self.__hide_line:
            if self.__visible:
                self.__visible = False
                self.__hide((self.__x1, self.__y1), self.__R, self.__br_size)
                self.__hide_line((self.__x1, self.__y1), (self.__x2, self.__y2), self.__br_size)

    def rotate(self, coord):
        if self.__draw_line and self.__hide_line and self.__visible:
            self.hide()
            self.calc_x2_pos(coord[0], coord[1])
            self.show()

    def move_up(self):
        if self.__draw_line and self.__hide_line and self.__visible:
            if (self.__y1 - self.__step - self.__R) > 0:
                self.hide()
                self.__y1 -= self.__step
                self.__y2 -= self.__step
                self.show()

    def move_down(self):
        if self.__draw_line and self.__hide_line and self.__visible:
            if (self.__y1 + self.__step + self.__R) < self.__max_y:
                self.hide()
                self.__y1 += self.__step
                self.__y2 += self.__step
                self.show()

    def move_right(self):
        if self.__draw_line and self.__hide_line and self.__visible:
            if (self.__x1 + self.__step + self.__R) < self.__max_x:
                self.hide()
                self.__x1 += self.__step
                self.__x2 += self.__step
                self.show()

    def move_left(self):
        if self.__draw_line and self.__hide_line and self.__visible:
            if (self.__x1 - self.__step - self.__R) > 0:
                self.hide()
                self.__x1 -= self.__step
                self.__x2 -= self.__step
                self.show()

    def shoot(self, mx, my):
        if self.__shooter and self.__visible:
            self.__shooter(self.__y2, self.__x2, mx, my)


    def belongs(self, x1, y1, x2, y2, xp, yp):
        if xp >= x1 and xp <= x2 and yp >= y1 and yp <= y2:
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
