from tkinter import *
from tkinter import ttk
from pubsub import pub 	# pip install PyPubSub
import tkinter.font as TkFont
from PIL import ImageTk,Image  # pip install pillow
# import functionss as funct


def donothing():
    print("Something happened...")


class View:
    def __init__(self, master, majorL, minorL):
        self.mainwin = master
        self.mainwin.title("Academic Advising Tool")
        self.mainwin.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))

        self.majorsList = majorL
        self.minorsList = minorL

        self.TNR20 = TkFont.Font(family='Times', size='20', weight='bold')
        self.TNR = TkFont.Font(family='Times')

        self.courseRow = 5
        self.courseCol = 4

        self.layout()
        self.menu()

    def layout(self):
        self.leftFrame = Frame(self.mainwin, highlightbackground='gray', highlightthickness=1)
        self.leftFrame.place(relwidth=0.48, relheight=0.98, relx=0.01, rely=0.02)

        self.rightFrame = Frame(self.mainwin, highlightbackground='gray', highlightthickness=1)
        self.rightFrame.place(relwidth=0.48, relheight=0.98, relx=0.5, rely=0.02)

        self.FourYearPlan()
        self.PlanningWorksheet_layout()

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
        # ============================ title ============================
        ProgPlanTitle = ttk.Label(self.rightFrame, text="Program Planning Worksheet", anchor=CENTER, font=('Helvetica', 19))
        ProgPlanTitle.place(rely=0.035, relx=0.30)

        # ============================ student name ============================
        nameFrame = Frame(self.rightFrame,)
        nameFrame.place(rely=0.1, relx=0.12)

        nameLabel = Label(nameFrame, text='Name:')
        nameLabel.pack(side=LEFT)

        self.nameEntry = ttk.Entry(nameFrame)
        self.nameEntry.pack()

        # ============================ student id ============================
        idFrame = Frame(self.rightFrame,)
        idFrame.place(rely=0.1, relx=0.5)

        idLabel = Label(idFrame, text='ID Number:')
        idLabel.pack(side=LEFT)

        self.idEntry = ttk.Entry(idFrame)
        self.idEntry.pack()

        # ============================ season ============================           TODO radio button
        seasonFrame = Frame(self.rightFrame, )
        seasonLabel = Label(seasonFrame, text='Registering for:')
        fallRadioBtn = ttk.Radiobutton(seasonFrame, text='Fall', value=1)
        summerRadioBtn = ttk.Radiobutton(seasonFrame, text='Summer', value=2)
        springRadioBtn = ttk.Radiobutton(seasonFrame, text='Spring', value=3)
        winterRadioBtn = ttk.Radiobutton(seasonFrame, text='Winter', value=4)

        seasonFrame.place(y=140, x=153, width=550)
        seasonLabel.pack(side=LEFT)
        fallRadioBtn.place(x=130)
        winterRadioBtn.place(x=210)
        springRadioBtn.place(x=310)
        summerRadioBtn.place(x=410)

        # ============================ major & minor ============================
        careerFrame = Frame(self.rightFrame)
        careerFrame.place(y=180, x=153, width=450)

        majorLabel = Label(careerFrame, text='Major(s): ')
        majorLabel.pack(side=LEFT)

        majorVar = StringVar()
        majorVar.set(self.majorsList[0])
        majorMenu = ttk.OptionMenu(careerFrame, majorVar, *self.majorsList)
        majorMenu.pack(side=LEFT)


        minorVar = StringVar()
        minorVar.set(self.minorsList[0])
        minorMenu = ttk.OptionMenu(careerFrame, minorVar, *self.minorsList)
        minorMenu.pack(side=RIGHT)

        minorLabel = Label(careerFrame, text='Minor(s): ')
        minorLabel.pack(side=RIGHT)

        # ============================ credits ============================
        credFrame = Frame(self.rightFrame,)
        credFrame.place(y=230, x=153, width=450)

        credLabel1 = Label(credFrame, text='Earned:')
        self.earnCredEntry = ttk.Entry(credFrame, width=3, state=DISABLED)
        credLabel2 = Label(credFrame, text='credits')

        credLabel1.pack(side=LEFT)
        self.earnCredEntry.pack(side=LEFT)
        credLabel2.pack(side=LEFT)

        credLabel3 = Label(credFrame, text='Currently Enrolled in')
        self.enrollCredEntry = ttk.Entry(credFrame, width=3)
        credLabel4 = Label(credFrame, text='credits')

        credLabel4.pack(side=RIGHT)
        self.enrollCredEntry.pack(side=RIGHT)
        credLabel3.pack(side=RIGHT)

        # ============================ Course table ============================
        courseTableFrameTitle = Frame(self.rightFrame)
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

        self.courseTableFrame = Frame(self.rightFrame, )
        self.courseTableFrame.place(rely=0.4, relx=0.12)

        self.courseEntry = [[]]
        for i in range(self.courseRow):
            self.courseEntry.append([])
            for j in range(self.courseCol):
                self.courseEntry[i].append(Entry(self.courseTableFrame, bd=3, width=12))
                self.courseEntry[i][j].grid(row=i, column=j)

    def populatePPW(self, arg1, arg2, arg3, arg4):    # (py dict, total cred, 2d course array, course size)
        # delete what was previously there then insert
        self.nameEntry.delete(0, END)
        self.nameEntry.insert(END, arg1['name'])

        self.idEntry.delete(0, END)
        self.idEntry.insert(END, arg1['s_id'])

        self.earnCredEntry['state'] = NORMAL
        self.earnCredEntry.delete(0, END)
        self.earnCredEntry.insert(END, arg1['credits'])
        self.earnCredEntry['state'] = 'readonly'

        self.enrollCredEntry.delete(0, END)
        self.enrollCredEntry.insert(END, arg2)

        for i in range (arg4):
            for j in range (self.courseCol):
                self.courseEntry[i][j].insert(END, arg3[i][j])

    # menus declaration
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