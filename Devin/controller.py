import tkinter as Tk
from model import Model
from view import View


class Controller:
    def __init__(self, parent):
        self.root = Tk.Tk()
        self.model = Model()
        # Pass to view links on root frame and controller object
        self.view = View(parent)
        self.root.title("Academic Advising Tool")
        self.root.geometry('1000x600')
        # self.root.deiconify()
        self.root.mainloop()