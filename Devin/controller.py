from tkinter import *
from model import Model
from view import View


class Controller:
    def __init__(self):
        self.root = Tk()
        self.root.title("Academic Advising Tool")
        self.root.geometry('1000x600')

        self.model = Model()
        self.view = View(self.root)
        # self.view.setup(self)
        self.root.mainloop()