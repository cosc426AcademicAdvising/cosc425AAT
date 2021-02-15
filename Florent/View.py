from tkinter import *
import tkinter as tk

def donothing():
    print("Something happened...")


class View:
    def __init__(self, master):
        self.container = master
        self.var = StringVar()

    def setup(self):    # run first
        # methods to setup user interface
        self.create_widgets()
        self.setup_menuBar()
        self.setup_layout()

    # temporary
    # open file browser and accept json
    def openFile(self):
        print("file browser")

    # testing function
    # goal: sent var to Controller so it can be set
    def getVar(self):
        self.var.set(
            " " * 8 + "Name : " + "AAA" + '\n' +
            "Student ID : " + "000" + "\t" * 3 + "Grad. Yr : " + "000" + '\n' +
            " " * 10 + "Year : " + "000"
        )

    def create_widgets(self):
        # frames
        self.leftFrame = Frame(self.container)
        self.topFrame = Frame(self.container)
        self.bottomFrame = Frame(self.container, bg='white')
        # student information in top frame
        self.studentInfoFrame = LabelFrame(self.topFrame)
        self.studentInfoLabel = Label(self.studentInfoFrame, textvariable=self.var, fg='black', bg='white', justify=LEFT)
        self.getVar() # functions for desired output

    def setup_menuBar(self):
        self.menuBar = Menu(self.container)
        self.container.config(menu=self.menuBar)
        # SCHEDULE MENU
        self.schedule = Menu(self.menuBar)
        self.menuBar.add_cascade(label='Schedule', menu=self.schedule)
        # dropdown
        self.schedule.add_command(label='New...', command=donothing)
        self.schedule.add_command(label='Open...', command=self.openFile)

        self.recent = Menu(self.schedule)
        self.schedule.add_cascade(label="Open recent...", menu=self.recent)
        self.recent.add_separator()
        self.recent.add_command(label='Clear', command=donothing)

        self.schedule.add_separator()
        self.schedule.add_command(label='Save', command=donothing)
        self.schedule.add_command(label="Save as...", command=donothing)
        self.schedule.add_separator()
        self.schedule.add_command(label='Export', command=donothing)
        self.schedule.add_command(label='Print', command=donothing)
        # MAJOR MENU
        self.major = Menu(self.menuBar)
        self.menuBar.add_cascade(label='Major', menu=self.major)
        # drop down

    def setup_layout(self):
        # frames
        self.leftFrame.place(relwidth=0.25, relheight=1)
        self.topFrame.place(relwidth=1, relheight=0.2, relx=0.25)
        self.bottomFrame.place(relwidth=0.75, relheight=0.8, relx=0.25, rely=0.2)

        self.studentInfoFrame.place(relwidth=0.4, relheight=0.7, relx=0.2, rely=0.1)
        self.studentInfoLabel.pack(fill=BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    # root.geometry("%sx%s" % (1000, 600))
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))  # fills whole window
    root.title("Academic Advising Tool")

    view = View(root)
    view.setup()
    root.mainloop()
