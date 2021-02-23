from tkinter import *
from tkinter import ttk
from pubsub import pub
import tkinter.font as TkFont


def donothing():
    print("Something happened...")


class View:
    def __init__(self, master):
        self.mainwin = master
        self.mainwin.title("Academic Advising Tool")
        self.mainwin.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))

        # fonts
        self.TNR20 = TkFont.Font(family='Times', size='20', weight='bold')
        self.TNR = TkFont.Font(family='Times')

        self.layout()
        self.menu()

    # widgets declarations
    def layout(self):
        self.leftFrame = Frame(self.mainwin, highlightbackground='gray', highlightthickness=1)
        self.rightFrame = Frame(self.mainwin, highlightbackground='gray', highlightthickness=1)

        self.studentInfoFrame = Frame(self.rightFrame, highlightbackground='gray', highlightthickness=1)

        self.set_layout()
        self.PlanningWorksheet_layout()

    # widgets positioning
    def set_layout(self):
        self.leftFrame.place(relwidth=0.48, relheight=0.98, relx=0.01, rely=0.02)
        self.rightFrame.place(relwidth=0.48, relheight=0.98, relx=0.5, rely=0.02)

    def PlanningWorksheet_layout(self):
        # *** title ***
        ProgPlanTitle = ttk.Label(self.rightFrame, text="Program Planning Worksheet",
                                       anchor=CENTER, font=self.TNR20)
        ProgPlanTitle.pack(side=TOP)

        # **** student name ****
        nameFrame = Frame(self.rightFrame,)
        nameLabel = Label(nameFrame, text='Name:')
        nameEntry = ttk.Entry(nameFrame)

        nameFrame.place(rely=0.05, relx=0.05)
        nameLabel.pack(side=LEFT)
        nameEntry.pack()

        # **** student id ****
        idFrame = Frame(self.rightFrame,)
        idLabel = Label(idFrame, text='ID Number:')
        idEntry = ttk.Entry(idFrame)

        idFrame.place(rely=0.05, relx=0.5)
        idLabel.pack(side=LEFT)
        idEntry.pack()

        # **** season ****
        seasonFrame = Frame(self.rightFrame,)
        seasonLabel = Label(seasonFrame, text='Registering for:')
        summerCkBt = ttk.Checkbutton(seasonFrame, text='Summer')
        fallCkBt = ttk.Checkbutton(seasonFrame, text='Fall')
        winterCkBt = ttk.Checkbutton(seasonFrame, text='Winter')
        springCkBt = ttk.Checkbutton(seasonFrame, text='Spring')

        seasonFrame.place(y=85, x=30, width=550)
        seasonLabel.pack(side=LEFT)
        summerCkBt.place(x=120)
        fallCkBt.place(x=220)
        winterCkBt.place(x=300)
        springCkBt.place(x=400)

        # **** major & minor ****
        majorFrame = Frame(self.rightFrame)
        majorFrame.place(y=130, x=30, width=450)

        majorLabel = Label(majorFrame, text='Major(s): ')

        majorsList = ['-', 'Computer Science', 'Math', 'Business']
        majorVar = StringVar()
        majorVar.set(majorsList[0])
        # use listbox instead because you can have more than one major
        majorMenu = ttk.OptionMenu(majorFrame, majorVar, *majorsList)
        majorLabel.pack(side=LEFT)
        majorMenu.pack(side=LEFT)

        minorLabel = Label(majorFrame, text='Minor(s): ')

        minorsList = ['-' , 'Computer Science', 'Math', 'Business']
        minorVar = StringVar()
        minorVar.set(minorsList[0])
        # use listbox instead because you can have more than one minor
        minorMenu = ttk.OptionMenu(majorFrame, minorVar, *minorsList)
        minorMenu.pack(side=RIGHT)
        minorLabel.pack(side=RIGHT)

        # **** credits ****
        credFrame = Frame(self.rightFrame,)
        credFrame.place(y=170, x=30, width=450)

        credLabel1 = Label(credFrame, text='Earned:')
        earncred = ttk.Entry(credFrame, width=3)
        credLabel2 = Label(credFrame, text='credits')

        credLabel1.pack(side=LEFT)
        earncred.pack(side=LEFT)
        credLabel2.pack(side=LEFT)

        credLabel3 = Label(credFrame, text='Currently Enrolled in')
        enrollcred = ttk.Entry(credFrame, width=3)
        credLabel4 = Label(credFrame, text='credits')

        credLabel4.pack(side=RIGHT)
        enrollcred.pack(side=RIGHT)
        credLabel3.pack(side=RIGHT)

    # menus declaration
    # each menu should have it own function where its drop down are declared
    def menu(self):
        menu = Menu(self.mainwin)
        self.mainwin.config(menu=menu)

        schedule = Menu(menu)
        menu.add_cascade(label='Schedule', menu=schedule)
        self.scheduleMenu(schedule)

        major = Menu(menu)
        menu.add_cascade(label='Load', menu=major)
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