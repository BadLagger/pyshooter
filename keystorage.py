import threading
import time

class KeyStorage:
    def __init__(self, key_bind):
        self.__key_array = []
        self.__key_th_arg = {}
        self.__key_th_arg["esc"] = False
        self.__key_th = threading.Thread(target=self.__thread, args=(self.__key_th_arg,))
        self.__key_th.start()
        self.__key_bind = key_bind

    def get_esc(self):
        return self.__key_th_arg["esc"]

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
            time.sleep(0.005)

    def __process(self, key):
        kb = self.__key_bind.get(key)
        if kb:
            kb["handler"](kb["object"])
