from tkinter import *


def donothing():
    print("Something happened...")


class View:
    def __init__(self, master):
        self.container = master

    def setup(self):    # run first
        # methods to setup user interface
        self.create_widgets()
        self.setup_menuBar()
        self.setup_layout()

    def create_widgets(self):
        # frames
        self.leftFrame = Frame(self.container, width=300, bg='blue')
        self.topFrame = Frame(self.container, height=100, bg='red')
        self.bottomFrame = Frame(self.container, height=500, bg='white')

    def setup_menuBar(self):
        self.menuBar = Menu(self.container)
        self.container.config(menu=self.menuBar)
        # file Menu
        self.schedule = Menu(self.menuBar)
        self.menuBar.add_cascade(label='Schedule', menu=self.schedule)
        # dropdown
        self.schedule.add_command(label='New...', command=donothing)
        self.schedule.add_command(label='Open...', command=donothing)
        # self.schedule.add_cascade(label="Open recent...", menu=self.schedule)
        self.schedule.add_separator()
        self.schedule.add_command(label='Save', command=donothing)
        self.schedule.add_command(label="Save as...", command=donothing)
        self.schedule.add_separator()
        self.schedule.add_command(label='Export', command=donothing)
        self.schedule.add_command(label='Print', command=donothing)
        # course menu

    def setup_layout(self):
        # frames
        self.leftFrame.pack(side=LEFT, fill=Y)
        self.topFrame.pack(side=TOP, fill=X)
        self.bottomFrame.pack(side=TOP, expand=True, fill=BOTH)


if __name__ == "__main__":
    root = Tk()
    root.geometry("%sx%s" % (1000, 600))
    root.title("Academic Advising Tool")

    view = View(root)
    view.setup()
    root.mainloop()
