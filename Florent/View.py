import tkinter as tk
from pubsub import pub      # pip install PyPubSub

def donothing():
    print("Something happened...")


class View:
    def __init__(self, container):
        self.container = container
        self.var = tk.StringVar()

    def setup(self):    # run first
        # methods to setup user interface
        self.create_widgets()
        self.setup_menuBar()
        self.setup_layout()

    def openSchedule(self):
        print("request student info")
        pub.sendMessage("request student info")     # msg key

    def setVar(self, data):
        self.var.set(
            "Name: " + data[0] + "\n" +
            "  ID: " + data[1] + "\n" +
            "Year: " + data[2]
        )

    def create_widgets(self):
        # frames
        self.leftFrame = tk.Frame(self.container, bg='gray')
        self.rightFrame = tk.Frame(self.container, bg='white')
        # student information in top frame
        self.studentInfoFrame = tk.Frame(self.rightFrame)
        self.studentInfoLabel = tk.Label(self.studentInfoFrame, textvariable=self.var, fg='black', bg='white', justify=tk.LEFT)

    def setup_menuBar(self):
        self.menuBar = tk.Menu(self.container)
        self.container.config(menu=self.menuBar)
        # SCHEDULE MENU
        self.schedule = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label='Schedule', menu=self.schedule)
        # dropdown
        self.schedule.add_command(label='New...', command=donothing)
        self.schedule.add_command(label='Open...', command=self.openSchedule)

        self.recent = tk.Menu(self.schedule)
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
        self.major = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label='Major', menu=self.major)
        # ADD CLASS MENU
        self.addClass = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label='Add Class', menu=self.addClass)

    def setup_layout(self):
            # Placing frames
            self.leftFrame.place(relwidth=0.48, relheight=0.98, rely=0.02, relx=0.01)
            self.rightFrame.place(relwidth=0.48, relheight=0.98, relx=0.5, rely=0.02)

            self.studentInfoFrame.place(relwidth=0.4, relheight=0.7, relx=0.2, rely=0.1)
            self.studentInfoLabel.pack()