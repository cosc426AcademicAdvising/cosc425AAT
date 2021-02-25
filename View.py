from tkinter import *
from tkinter import ttk
from pubsub import pub 	# pip install PyPubSub
import functionss as funct
import tkinter.font as TkFont

from PIL import ImageTk,Image  # pip install pillow



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
        self.FourYearPlan()
        self.PlanningWorksheet_layout()

    # widgets positioning
    def set_layout(self):
        self.leftFrame.place(relwidth=0.48, relheight=0.98, relx=0.01, rely=0.02)
        self.rightFrame.place(relwidth=0.48, relheight=0.98, relx=0.5, rely=0.02)

    def FourYearPlan(self):
        self.image = Image.open("CS4YrPlan.png")
        self.background_image = ImageTk.PhotoImage(self.image)
        self.img_copy = self.image.copy()

        self.background = Label(self.leftFrame, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)

    def PlanningWorksheet_layout(self):
        # *** title ***
        ProgPlanTitle = ttk.Label(self.rightFrame, text="Program Planning Worksheet",
                                       anchor=CENTER, font="Arial")
        ProgPlanTitle.place(rely=0.035, relx=0.35)

        # **** student name ****
        nameFrame = Frame(self.rightFrame,)
        nameLabel = Label(nameFrame, text='Name:')
        self.nameEntry = ttk.Entry(nameFrame)

        nameFrame.place(rely=0.1, relx=0.12)
        nameLabel.pack(side=LEFT)
        self.nameEntry.pack()

        # **** student id ****
        idFrame = Frame(self.rightFrame,)
        idLabel = Label(idFrame, text='ID Number:')
        self.idEntry = ttk.Entry(idFrame)

        idFrame.place(rely=0.1, relx=0.5)
        idLabel.pack(side=LEFT)
        self.idEntry.pack()

        # **** season ****                                  TODO radio button
        seasonFrame = Frame(self.rightFrame,)
        seasonLabel = Label(seasonFrame, text='Registering for:')
        summerCkBt = ttk.Checkbutton(seasonFrame, text='Summer')
        fallCkBt = ttk.Checkbutton(seasonFrame, text='Fall')
        winterCkBt = ttk.Checkbutton(seasonFrame, text='Winter')
        springCkBt = ttk.Checkbutton(seasonFrame, text='Spring')

        seasonFrame.place(y=135, x=106, width=550)
        seasonLabel.pack(side=LEFT)
        summerCkBt.place(x=130)
        fallCkBt.place(x=230)
        winterCkBt.place(x=310)
        springCkBt.place(x=410)

        # **** major & minor ****
        majorFrame = Frame(self.rightFrame)
        majorFrame.place(y=180, x=106, width=450)

        majorLabel = Label(majorFrame, text='Major(s): ')

        majorsList = funct.listAllMajors()     #  from functionss.py
        majorVar = StringVar()
        majorVar.set(majorsList[0])
        majorMenu = ttk.OptionMenu(majorFrame, majorVar, *majorsList)
        majorLabel.pack(side=LEFT)
        majorMenu.pack(side=LEFT)

        minorLabel = Label(majorFrame, text='Minor(s): ')

        minorsList = funct.listAllMinors()      # from functionss.py
        minorVar = StringVar()
        minorVar.set(minorsList[0])
        minorMenu = ttk.OptionMenu(majorFrame, minorVar, *minorsList)
        minorMenu.pack(side=RIGHT)
        minorLabel.pack(side=RIGHT)

        # **** credits ****
        credFrame = Frame(self.rightFrame,)
        credFrame.place(y=230, x=106, width=450)

        credLabel1 = Label(credFrame, text='Earned:')
        self.earncred = ttk.Entry(credFrame, width=3)
        credLabel2 = Label(credFrame, text='credits')

        credLabel1.pack(side=LEFT)
        self.earncred.pack(side=LEFT)
        credLabel2.pack(side=LEFT)

        credLabel3 = Label(credFrame, text='Currently Enrolled in')
        self.enrollcred = ttk.Entry(credFrame, width=3)
        credLabel4 = Label(credFrame, text='credits')

        credLabel4.pack(side=RIGHT)
        self.enrollcred.pack(side=RIGHT)
        credLabel3.pack(side=RIGHT)

        # **** Course table titles for cols ****
        courseTableFrameTitle = Frame(self.rightFrame, )
        courseTableFrameTitle.place(rely=0.37, relx=0.12)

        courseNumLabel = Label(courseTableFrameTitle, text='Course Number              Course Title '
                                                           '                        '
                                                           'Credit Hours                    Gen Ed Group/Elective')
        # courseTitleLabel = Label(courseTableFrameTitle, text='Course Title', padx=0.5, pady=0.01)
        # courseCreditHrLabel = Label(courseTableFrameTitle, text='Credit Hours', padx=0.5, pady=0.01)
        # courseGenEdGrpLabel = Label(courseTableFrameTitle, text='Gen Ed Group', padx=0.5, pady=0.01)

        courseNumLabel.pack(side=LEFT)
        # courseTitleLabel.pack(side=LEFT, padx=0.5, pady=0.01)
        # courseCreditHrLabel.pack(side=LEFT, padx=0.5, pady=0.01)
        # courseGenEdGrpLabel.pack(side=LEFT, padx=0.5, pady=0.01)

        # **** Course table for Course number****
        self.courseTableFrame = Frame(self.rightFrame, )
        self.courseTableFrame.place(rely=0.4, relx=0.12)

        #for i in range (7):
            #for j in range (4):
                #if j==0:
                    #self.courseNumEntry = (Entry(courseTableFrame, bd=3, width=12))
                    #self.courseNumEntry.grid(row=i, column=j)
                #else:
                    #self.courseNumEntry = (Entry(courseTableFrame, bd=3))
                    #self.courseNumEntry.grid(row=i, column=j)
                    # courseNumEntry.insert(END, courseNumLabelArr[i][j])

    def populatePPW(self, arg1, arg2, arg3, arg4):    # py dict, total cred, 2d course array, course size
        # delete what was previously there then insert
        self.nameEntry.delete(0, END)
        self.nameEntry.insert(END, arg1['student']['name'])

        self.idEntry.delete(0, END)
        self.idEntry.insert(END, arg1['student']['id'])

        self.enrollcred.delete(0, END)
        self.enrollcred.insert(END, arg2)

        # table
        for i in range (arg4):
            for j in range (4):
                if j == 0:
                    courseEntry = (Entry(self.courseTableFrame, bd=3, width=12))
                    courseEntry.grid(row=i, column=j)
                    courseEntry.insert(END, arg3[i][j])
                elif j == 2:
                    courseEntry = (Entry(self.courseTableFrame, bd=3, width=3))
                    courseEntry.grid(row=i, column=j)
                    courseEntry.insert(END, arg3[i][j])
                else:
                    courseEntry = (Entry(self.courseTableFrame, bd=3))
                    courseEntry.grid(row=i, column=j)
                    courseEntry.insert(END, arg3[i][j])

    # menus declaration
    # each menu should have it own function where its drop down are declared
    def menu(self):
        menu = Menu(self.mainwin)
        self.mainwin.config(menu=menu)

        schedule = Menu(menu)
        menu.add_cascade(label='Schedule', menu=schedule)
        self.scheduleMenu(schedule)

        load = Menu(menu)
        menu.add_cascade(label='View', menu=load)
        self.loadMenu(load)

        DB = Menu(menu)
        menu.add_cascade(label='Update DB', menu=DB)
        self.DataBaseMenu(DB)

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

    # load menu drop down
    def loadMenu(self, major):
        major.add_command(label='Four Year Plan')
        major.add_command(label='Course Taken List')
        major.add_separator()
        major.add_command(label='Major Checklist')
        major.add_command(label='Minor Checklist')

    # data base menu dropdown
    def DataBaseMenu(self, DB):
        DB.add_command(label='Current Semester Course')
        DB.add_separator()
        DB.add_command(label='Add/Remove a Department')
        DB.add_command(label='Add/remove a Major')
        DB.add_command(label='Add/Remove a minor')

    def newSchedule(self):
        pub.sendMessage("New Menu Dropdown Pressed")

    def openSchedule(self):
        pub.sendMessage("request_PPW")

    def openRecentSchedule(self):
        print("Open schedule")

    def saveSchedule(self):
        print("Saved schedule")

    def saveAsSchedule(self):
        print("Save schedule as..")

    def exportSchedule(self):
        print("Export schedule")

    def printSchedule(self):
        print("Print schedule")