class Bullet:
    def __init__(self):
        self.__b_len = 0
        self.__path_discrete = 0
        self.__bgn_px = None
        self.__bgn_py = None
        self.__cur_px = None
        self.__cur_py = None
        self.__end_px = None
        self.__end_py = None
        self.__b_line = None
        self.__path_len = None

    def __get_line_len(self, x1, y1, x2, y2):
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def set_len(self, l):
        if l > 0:
            self.__b_len = l
            if self.__path_discrete == 0:
                self.__path_discrete = self.__b_len
        else:
            raise ValueError

    def set_discrete(self, d):
        if d > 0:
            self.__path_discrete = d
        else:
            self.__path_discrete = self.__b_len

    def set_bgn_point(self, px, py):
        self.__bgn_px = px
        self.__bgn_py = py

    def set_end_point(self, px, py):
        self.__end_px = px
        self.__end_py = py

    def get_next_pos(self):
        if self.__bgn_px != self.__end_px:
            ax = self.__end_px - self.__bgn_px
            ay = self.__end_py - self.__bgn_py
            a = ay / ax
            x = ((self.__b_len * ax) / ((ax ** 2 + ay ** 2) ** 0.5 )) + self.__bgn_px
            y = a * (x - self.__bgn_px) + self.__bgn_py
            self.__b_line = [(self.__bgn_py, self.__bgn_px),(y, x)]
            if ax >= 0:
                if x < self.__end_px:
                    self.__bgn_px = x
                    self.__bgn_py = y
                else:
                    self.__bgn_px = self.__end_px
                    self.__bgn_py = self.__end_py
            else:
                if x > self.__end_px:
                    self.__bgn_px = x
                    self.__bgn_py = y
                else:
                    self.__bgn_px = self.__end_px
                    self.__bgn_py = self.__end_py
            return self.__b_line
        self.__path_len = None
        return None

    def get_last_pos(self):
        return self.__b_line
