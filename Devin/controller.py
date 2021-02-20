from tkinter import *
from model import Model
from view import View


class Controller:
    def __init__(self):
        self.root = Tk()
        self.root.title("Academic Advising Tool")
        self.root.geometry('1000x600')

        # child window
        self.my_w_child = Toplevel(self.root)  # Child window
        self.my_w_child.geometry("200x200")  # Size of the window
        self.my_w_child.title("www.plus2net.com")

        self.model = Model()
        self.view = View(self.root)
        self.view.setup()
        self.root.mainloop()