from tkinter import *


def donothing():
    print("Something happened...")


class View:
    def __init__(self, master):
        self.container = master

    def setup(self):    # run first
        # methods to setup user interface
        self.create_widgets()
        self.setup_layout()
        self.setup_menuBar()

    def create_widgets(self):
        # frames
        self.leftFrame = Frame(self.container, bg='gray')
        self.topFrame = Frame(self.container, bg='white')
        self.bottomFrame = Frame(self.container, bg='black')
        # student information in top frame
        self.studentInfoFrame = LabelFrame(self.topFrame)
        self.studentInfoLabel = Label(self.studentInfoFrame, textvariable="Im here", fg='black', bg='white', justify=LEFT)
        # select courses in left frame
        self.selectCourseFrame = LabelFrame(self.leftFrame)
        self.selectCourseLabel = Label(self.selectCourseFrame, textvariable="Im here", fg='black', bg='white', justify=LEFT)

        self.selectCourseEntry = Entry(self.leftFrame)

    def setup_layout(self):
        # frames
        self.leftFrame.place(relwidth=0.25, relheight=1)
        self.topFrame.place(relwidth=1, relheight=0.2, relx=0.25)
        self.bottomFrame.place(relwidth=0.75, relheight=0.8, relx=0.25, rely=0.2)

        # labels
        self.studentInfoFrame.place(relwidth=0.4, relheight=0.7, relx=0.2, rely=0.1)
        self.studentInfoLabel.pack(fill=BOTH, expand=True)

        self.selectCourseFrame.place(relx=0.055, rely=0.5, relwidth=0.75, relheight=0.45)
        self.selectCourseLabel.pack(fill=BOTH, expand=True)

        # Entry box
        self.selectCourseEntry.place(relx=0.055, rely=0.46, relwidth=0.75, relheight=0.04)

        # recent schedule list on left hand side
        self.scrollbar = Scrollbar(self.leftFrame, bg='gray')
        self.scrollbar.place(relx=0.75, rely=0.035, relwidth=0.08, relheight=0.4)

        self.recent_list = Listbox(self.leftFrame, yscrollcommand=self.scrollbar.set, highlightcolor='#8a0000', highlightthickness=4.0, selectbackground='gray', bg='#a8a8a8')
        # Filling list with schedules ******NEEDS TO BE PUT IN MODEL CLASS******
        for i in range(30):
            self.recent_list.insert(END, "Schedule " + str(i))
        # ********************************************************************
        self.recent_list.place(relx=0.05, rely=0.035, relwidth=0.7, relheight=0.4)
        # Connecting list and scrollbar functionality
        self.scrollbar.config(command=self.recent_list.yview)

    def setup_menuBar(self):
        self.menuBar = Menu(self.container)
        self.container.config(menu=self.menuBar)
        # SCHEDULE MENU
        self.schedule = Menu(self.menuBar)
        self.menuBar.add_cascade(label='Schedule', menu=self.schedule)
        # dropdown
        self.schedule.add_command(label='New...', command=donothing)
        self.schedule.add_command(label='Open...', command=donothing)

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