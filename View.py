from tkinter import *
from tkinter import ttk
from pubsub import pub


def donothing():
    print("Something happened...")


class View:
    def __init__(self, master):
        self.mainwin = master
        self.mainwin.title("Academic Advising Tool")
        self.mainwin.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))

        self.layout()
        self.menu()

    # widgets declarations
    def layout(self):
        self.leftFrame = Frame(self.mainwin, highlightbackground='gray', highlightthickness=1)
        self.rightFrame = Frame(self.mainwin, highlightbackground='gray', highlightthickness=1)

        self.studentInfoFrame = Frame(self.rightFrame, highlightbackground='gray', highlightthickness=1)

        self.set_layout()

    # widgets positioning
    def set_layout(self):
        self.leftFrame.place(relwidth=0.48, relheight=0.98, relx=0.01, rely=0.02)
        self.rightFrame.place(relwidth=0.48, relheight=0.98, relx=0.5, rely=0.02)

        self.studentInfoFrame.place(relwidth=0.8, relheight=0.18, relx=0.1, rely=0.04)

    # menus declaration
    # each menu should have it own function where its drop down are declared
    def menu(self):
        menu = Menu(self.mainwin)
        self.mainwin.config(menu=menu)

        schedule = Menu(menu)
        menu.add_cascade(label='Schedule', menu=schedule)
        self.scheduleMenu(schedule)

        major = Menu(menu)
        menu.add_cascade(label='Major', menu=major)
        self.majorMenu(major)

    # schedule menu dropdown
    def scheduleMenu(self, schedule):
        schedule.add_command(label='New...', command=donothing)
        schedule.add_command(label='Open...', command=donothing)

        recent = Menu(schedule)
        schedule.add_cascade(label="Open recent...", menu=recent)
        recent.add_separator()
        recent.add_command(label='Clear', command=donothing)

        schedule.add_separator()
        schedule.add_command(label='Save', command=donothing)
        schedule.add_command(label="Save as...", command=donothing)
        schedule.add_separator()
        schedule.add_command(label='Export', command=donothing)
        schedule.add_command(label='Print', command=donothing)

    def majorMenu(self, major):
        return