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
        self.majorDropdown()
        self.minorDropdown()

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
        schedule.add_command(label='New...', command=self.newSchedule)
        schedule.add_command(label='Open...', command=self.openSchedule)

        recent = Menu(schedule)
        schedule.add_cascade(label="Open recent...", menu=recent)
        recent.add_separator()
        recent.add_command(label='Clear', command=self.openRecentSchedule)

        schedule.add_separator()
        schedule.add_command(label='Save', command=self.saveSchedule)
        schedule.add_command(label="Save as...", command=self.saveAsSchedule)
        schedule.add_separator()
        schedule.add_command(label='Export', command=self.exportSchedule)
        schedule.add_command(label='Print', command=self.printSchedule)

    def majorDropdown(self):
        majorsList = ['Computer Science', 'Math', 'Business']
        self.major = StringVar()
        self.major.set(majorsList[1])
        self.major = OptionMenu(self.rightFrame, self.major, *majorsList)
        self.major.pack()

    def minorDropdown(self):
        majorsList = ['Computer Science', 'Math', 'Business']
        self.major = StringVar()
        self.major.set(majorsList[1])
        self.major = OptionMenu(self.rightFrame, self.major, *majorsList)
        self.major.pack()

    def newSchedule(self):
        pub.sendMessage("New Menu Dropdown Pressed")

    def openSchedule(self):
        print("Open schedule")

    def openRecentSchedule(self):
        print("Open schedule")

    def saveSchedule(self):
        print("Saved schedule")

    def saveAsSchedule(self):
        print("Save schedule as..")

    def exportSchedule(self):
        print("Export schedule")

    def printSchedule(self):
        print("Print scedule")

    def majorMenu(self, major):
        return