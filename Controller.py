from View import View
from Model import Model

from tkinter import *
from pubsub import pub


class Controller:
    def __init__(self, master):
        self.view = View(master)
        self.model = Model()


if __name__=="__main__":
    root = Tk()
    app = Controller(root)
    root.mainloop()