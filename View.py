from tkinter import *
from tkinter import ttk
# from ttkthemes import ThemedTk
from pubsub import pub  # pip install PyPubSub
import tkinter.font as TkFont
# from PIL import ImageTk, Image  # pip install pillow


# import functionss as funct


def donothing():
    print("Something happened...")


class View:
    def __init__(self, master, majorL, minorL):
        self.mainwin = master
        self.mainwin.title("Academic Advising Tool")
        self.mainwin.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))
        self.mainwin.minsize(width=master.winfo_screenwidth(), height=master.winfo_screenheight())
        self.mainwin.maxsize(width=master.winfo_screenwidth(), height=master.winfo_screenheight())

        self.majorsList = majorL
        self.minorsList = minorL

        self.TNR20 = TkFont.Font(family='Times', size='20', weight='bold')
        self.TNR = TkFont.Font(family='Times')

        self.layout()
        self.menu()

    def layout(self):
        self.leftFrame = Frame(self.mainwin, highlightbackground='gray', highlightthickness=1)
        self.leftFrame.place(relwidth=0.48, relheight=0.98, relx=0.01, rely=0.02)

        self.rightFrame = Frame(self.mainwin, highlightbackground='gray', highlightthickness=1)
        self.rightFrame.place(relwidth=0.48, relheight=0.98, relx=0.5, rely=0.02)
        # self.rightFrame.rowconfigure(1, weight=1)

        self.FourYearPlan()
        self.PlanningWorksheet_layout()

    def FourYearPlan(self):
        '''
        # outer most blank frames left & right
        width = self.mainwin.winfo_screenwidth()
        height = self.mainwin.winfo_screenheight()
        AspectRatio = width/height

        if AspectRatio == 16/10:
            blank1 = Frame(self.leftFrame, width=50).grid(column=0, row=0, rowspan=30, sticky=(N,E,S,W))
            blank2 = Frame(self.leftFrame, width=50).grid(column=5, row=0, rowspan=30, sticky=(N,E,S,W))
        elif AspectRatio == 16/9:
            blank1 = Frame(self.leftFrame, width=190).grid(column=0, row=0,rowspan=30,sticky=(N, E, S, W))
            blank2 = Frame(self.leftFrame, width=190).grid(column=5, row=0, rowspan=30,sticky=(N, E, S, W))
        elif AspectRatio == 4/3:
            blank1 = Frame(self.leftFrame, width=200).grid(column=0, row=0,rowspan=30,sticky=(N, E, S, W))
            blank2 = Frame(self.leftFrame, width=160).grid(column=5, row=0, rowspan=30,sticky=(N, E, S, W))
        elif AspectRatio == 3/2:
            blank1 = Frame(self.leftFrame, width=160).grid(column=0, row=0,rowspan=30,sticky=(N, E, S, W))
            blank2 = Frame(self.leftFrame, width=160).grid(column=5, row=0, rowspan=30,sticky=(N, E, S, W))
        else:
            blank1 = Frame(self.leftFrame, width=50).grid(column=0, row=0, rowspan=30, sticky=(N, E, S, W))
            blank2 = Frame(self.leftFrame, width=50).grid(column=5, row=0, rowspan=30, sticky=(N, E, S, W))

        self.leftFrame.update()
        h = self.leftFrame.winfo_height() * .028
        blank3 = Frame(self.leftFrame, height=h).grid(row=1, column=0, columnspan=5) # before name id
        blank4 = Frame(self.leftFrame, height=h).grid(row=3, column=0, columnspan=5) # before seasons
        blank5 = Frame(self.leftFrame, height=h).grid(row=5, column=0, columnspan=5) # before major minor
        blank6 = Frame(self.leftFrame, height=h).grid(row=7, column=0, columnspan=5) # before cred frame
        blank7 = Frame(self.leftFrame, height=h).grid(row=9, column=0, columnspan=5) # before enrollment date
        blank8 = Frame(self.leftFrame, height=h).grid(row=11, column=0, columnspan=5) # before table
        blank9 = Frame(self.leftFrame, height=h).grid(row=14, column=0, columnspan=5)  # before memo

        '''
        # ============================ Scroll Bar ============================
        self.canvas = Canvas(self.leftFrame)
        self.canvas.pack(side=LEFT, fill="both", expand=True)

        self.scrollbar = Scrollbar(self.leftFrame, orient="vertical")
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.innerLeftFrame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.innerLeftFrame, anchor=NW)

        # ============================ title ============================
        ProgPlanTitle = ttk.Label(self.innerLeftFrame, text="Program Planning Worksheet", anchor=CENTER,
                                  font=('Helvetica', 19))
        ProgPlanTitle.place(x=300, y=30)

        # ============================ student name ============================
        nameFrame = Frame(self.innerLeftFrame)
        nameFrame.place(x=210, y=100)

        nameLabel = Label(nameFrame, text='Name:')
        nameLabel.pack(side=LEFT)

        self.nameEntry = ttk.Entry(nameFrame)
        self.nameEntry.pack()

        # ============================ student id ============================
        idFrame = Frame(self.innerLeftFrame)
        idFrame.place(x= 510, y= 100)

        idLabel = Label(idFrame, text='ID Number:')
        idLabel.pack(side=LEFT)

        self.idEntry = ttk.Entry(idFrame, width=8)
        self.idEntry.pack()

        # ============================ Year Tables ============================
        self.createTable("Semester 1: ", 45, 200)
        self.createTable("Semester 2: ", 475, 200)
        self.createTable("Semester 3: ", 45, 450)
        self.createTable("Semester 4: ", 475, 450)
        self.createTable("Semester 5: ", 45, 700)
        self.createTable("Semester 6: ", 475, 700)

    def PlanningWorksheet_layout(self):
        # outer most blank frames left & right
        width = self.mainwin.winfo_screenwidth()
        height = self.mainwin.winfo_screenheight()
        AspectRatio = width/height

        if AspectRatio == 16/10:
            blank1 = Frame(self.rightFrame, width=50).grid(column=0, row=0, rowspan=30, sticky=(N,E,S,W))
            blank2 = Frame(self.rightFrame, width=50).grid(column=5, row=0, rowspan=30, sticky=(N,E,S,W))
        elif AspectRatio == 16/9:
            blank1 = Frame(self.rightFrame, width=190).grid(column=0, row=0,rowspan=30,sticky=(N, E, S, W))
            blank2 = Frame(self.rightFrame, width=190).grid(column=5, row=0, rowspan=30,sticky=(N, E, S, W))
        elif AspectRatio == 4/3:
            blank1 = Frame(self.rightFrame, width=200).grid(column=0, row=0,rowspan=30,sticky=(N, E, S, W))
            blank2 = Frame(self.rightFrame, width=160).grid(column=5, row=0, rowspan=30,sticky=(N, E, S, W))
        elif AspectRatio == 3/2:
            blank1 = Frame(self.rightFrame, width=160).grid(column=0, row=0,rowspan=30,sticky=(N, E, S, W))
            blank2 = Frame(self.rightFrame, width=160).grid(column=5, row=0, rowspan=30,sticky=(N, E, S, W))
        else:
            blank1 = Frame(self.rightFrame, width=50).grid(column=0, row=0, rowspan=30, sticky=(N, E, S, W))
            blank2 = Frame(self.rightFrame, width=50).grid(column=5, row=0, rowspan=30, sticky=(N, E, S, W))

        self.rightFrame.update()
        h = self.rightFrame.winfo_height() * .028
        blank3 = Frame(self.rightFrame, height=h).grid(row=1, column=0, columnspan=5) # before name id
        blank4 = Frame(self.rightFrame, height=h).grid(row=3, column=0, columnspan=5) # before seasons
        blank5 = Frame(self.rightFrame, height=h).grid(row=5, column=0, columnspan=5) # before major minor
        blank6 = Frame(self.rightFrame, height=h).grid(row=7, column=0, columnspan=5) # before cred frame
        blank7 = Frame(self.rightFrame, height=h).grid(row=9, column=0, columnspan=5) # before enrollment date
        blank8 = Frame(self.rightFrame, height=h).grid(row=11, column=0, columnspan=5) # before table
        blank9 = Frame(self.rightFrame, height=h).grid(row=14, column=0, columnspan=5)  # before memo


        # ============================ title ============================
        ProgPlanTitle = ttk.Label(self.rightFrame, text="Program Planning Worksheet", anchor=CENTER,
                                  font=('Helvetica', 19))
        ProgPlanTitle.grid(row=0, column=2, columnspan=3)

        # ============================ student name ============================
        nameFrame = Frame(self.rightFrame)
        nameFrame.grid(row=2, column=1, columnspan=2)

        nameLabel = Label(nameFrame, text='Name:')
        nameLabel.pack(side=LEFT)

        self.nameEntry = ttk.Entry(nameFrame)
        self.nameEntry.pack()

        # ============================ student id ============================
        idFrame = Frame(self.rightFrame)
        idFrame.grid(row=2, column=3, columnspan=2)

        idLabel = Label(idFrame, text='ID Number:')
        idLabel.pack(side=LEFT)

        self.idEntry = ttk.Entry(idFrame, width=8)
        self.idEntry.pack()

        # ============================ season ============================
        self.seasonVar = StringVar()

        seasonFrame = Frame(self.rightFrame, )
        seasonLabel = Label(seasonFrame, text='Registering for:')
        fallRadioBtn = ttk.Radiobutton(seasonFrame, text='Fall', variable=self.seasonVar, value='Fall')
        summerRadioBtn = ttk.Radiobutton(seasonFrame, text='Summer', variable=self.seasonVar, value='Summer')
        springRadioBtn = ttk.Radiobutton(seasonFrame, text='Spring', variable=self.seasonVar, value='Spring')
        winterRadioBtn = ttk.Radiobutton(seasonFrame, text='Winter', variable=self.seasonVar, value='Winter')

        seasonFrame.grid(row=4, column=1, columnspan=4)
        seasonLabel.grid(row=0, column=0, padx=10)
        fallRadioBtn.grid(row=0, column=1, padx=10)
        winterRadioBtn.grid(row=0, column=2, padx=10)
        springRadioBtn.grid(row=0, column=3, padx=10)
        summerRadioBtn.grid(row=0, column=4)

        # ============================ major & minor ============================
        careerFrame = Frame(self.rightFrame)
        careerFrame.grid(row=6, column=1, columnspan=4)

        majorLabel = Label(careerFrame, text='Major(s): ')
        majorLabel.grid(row=0, column=0)

        self.majorVar = StringVar()
        self.majorVar.set(self.majorsList[0])
        majorMenu = ttk.OptionMenu(careerFrame, self.majorVar, *self.majorsList)
        majorMenu.grid(row=0, column=1)

        mblank = Frame(careerFrame, width=75).grid(row=0, column=2)

        self.minorVar = StringVar()
        self.minorVar.set(self.minorsList[0])
        minorMenu = ttk.OptionMenu(careerFrame, self.minorVar, *self.minorsList)
        minorMenu.grid(row=0, column=4)

        minorLabel = Label(careerFrame, text='Minor(s): ')
        minorLabel.grid(row=0, column=3)

        # ============================ credits ============================
        credFrame = Frame(self.rightFrame, )
        credFrame.grid(row=8, column=1, columnspan=4)

        credLabel1 = Label(credFrame, text='Earned:')
        self.earnCredEntry = ttk.Entry(credFrame, width=3, justify=CENTER, state=DISABLED)
        credLabel2 = Label(credFrame, text='credits')

        credLabel1.grid(row=0, column=0)
        self.earnCredEntry.grid(row=0, column=1)
        credLabel2.grid(row=0, column=2)

        cblank = Frame(credFrame, width=130).grid(row=0, column=3)

        credLabel3 = Label(credFrame, text='Currently Enrolled in')
        self.enrollCredEntry = ttk.Entry(credFrame, width=3, justify=CENTER)
        credLabel4 = Label(credFrame, text='credits')

        credLabel4.grid(row=0, column=4)
        self.enrollCredEntry.grid(row=0, column=5)
        credLabel3.grid(row=0, column=6)

        # ====================== Enrollment Date ========================
        enrlDateFrame = ttk.Frame(self.rightFrame)
        enrlDateFrame.grid(row=10, column=2, columnspan=2)

        enrlDate = Label(enrlDateFrame, text='Enrollment Date:')
        enrlDate.pack(side=LEFT)

        self.enrlDateEntry = ttk.Entry(enrlDateFrame, width=5)
        self.enrlDateEntry.pack()

        # ============================ Course table ============================
        courseTableFrame = Frame(self.rightFrame, )
        courseTableFrame.grid(row=12, column=1, columnspan=4)

        self.courseTree = ttk.Treeview(courseTableFrame, height=7) # TIP: height is number of rows
        self.courseTree.pack()

        self.courseTree['columns'] = ("course#", "title", "cred", "gen/elect")

        self.courseTree.column("#0", width=0, stretch=NO)   # important
        self.courseTree.column("course#", anchor=CENTER, width=100) # anchor for the data in the column
        self.courseTree.column("title", anchor=W, width=200)
        self.courseTree.column("cred", anchor=CENTER, width=100)
        self.courseTree.column("gen/elect", anchor=CENTER, width=100)

        self.courseTree.heading("course#", text='Course Number', anchor=CENTER) # anchor for the title of the column
        self.courseTree.heading("title", text='Title', anchor=CENTER)
        self.courseTree.heading("cred", text='Credit Hours', anchor=CENTER)
        self.courseTree.heading("gen/elect", text='Gen ed/Elect', anchor=CENTER)

        # ===================== backup course ===================
        backupCourseFrame = Frame(self.rightFrame)
        backupCourseFrame.grid(row=13, column=1, columnspan=4)

        backuplabel = Label(backupCourseFrame, text="Back-up Courses").pack(anchor=CENTER)

        self.backupCourseTree = ttk.Treeview(backupCourseFrame, height=2)
        self.backupCourseTree.pack()

        self.backupCourseTree['columns'] = ("course#", "title", "cred", "gen/elect")

        self.backupCourseTree.column("#0", width=0, stretch=NO)
        self.backupCourseTree.column("course#", anchor=CENTER, width=100)
        self.backupCourseTree.column("title", anchor=W, width=200)
        self.backupCourseTree.column("cred", anchor=CENTER, width=100)
        self.backupCourseTree.column("gen/elect", anchor=CENTER, width=100)

        # ====================== memo ========================
        memoFrame = ttk.LabelFrame(self.rightFrame, text='Memo:')
        memoFrame.grid(row=15, column=2, columnspan=2)

        self.memoEntry = Text(memoFrame, width=50, height=5)
        self.memoEntry.pack()

    def populatePPW(self, arg1, arg2, arg3, arg4, arg5):  # (py dict, total cred, 2d course array, course size)
        # delete what was previously there then insert
        self.nameEntry.delete(0, END)
        self.nameEntry.insert(END, arg1['name'])

        self.idEntry.delete(0, END)
        self.idEntry.insert(END, arg1['s_id'])

        self.seasonVar.set(arg1['registering_for'])

        cnt = len(self.majorsList)
        index = 0
        for i in range(cnt):
            if arg1['major'] == self.majorsList[i]:
                index = i
        self.majorVar.set(self.majorsList[index])

        cnt = len(self.minorsList)
        index = 0
        for i in range(cnt):
            if arg1['minor'] == self.minorsList[i]:
                index = i
        self.minorVar.set(self.minorsList[index])

        self.earnCredEntry['state'] = NORMAL
        self.earnCredEntry.delete(0, END)
        self.earnCredEntry.insert(END, arg1['credits'])
        self.earnCredEntry['state'] = 'readonly'

        self.enrollCredEntry.delete(0, END)
        self.enrollCredEntry.insert(END, arg2)

        self.enrlDateEntry.delete(0, END)
        self.enrlDateEntry.insert(END, arg1['enrll'])

        self.memoEntry.delete('1.0', 'end')
        self.memoEntry.insert('1.0', arg1['memo'])

        c_counter = 0
        # when inserting 'iid' needs to be different
        for c in arg3:
            self.courseTree.insert(parent='', index='end', iid=c_counter, text="", values=(c[0],c[1],c[2],c[3]))
            c_counter += 1

        c_counter = 0
        for c in arg5:
            self.backupCourseTree.insert(parent='', index='end', iid=c_counter, text="", values=(c[0],c[1],c[2],c[3]))
            c_counter += 1

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

        theme = Menu(menu)
        menu.add_cascade(label='Themes', menu=theme)
        self.themeMenu(theme)

    def themeMenu(self, theme):
        #s = ThemedTk(self.mainwin)
        '''
        def lightMode(s):
            s.set_theme("plastik")

        def darkMode(s):
            s.set_theme("black")
        '''
        #theme.add_command(label='Light Mode', command=)
        theme.add_command(label='Dark Mode')

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
        # pub.sendMessage("New Menu Dropdown Pressed")
        self.nameEntry.delete(0, END)
        self.idEntry.delete(0, END)
        self.seasonVar.set('')

        self.earnCredEntry['state'] = NORMAL
        self.earnCredEntry.delete(0, END)
        self.earnCredEntry['state'] = 'readonly'

        self.enrollCredEntry.delete(0, END)

        self.enrlDateEntry.delete(0, END)

        self.memoEntry.delete('1.0', 'end')

        ''''                                                            TODO clear Treeview
        for i in range(self.courseRow):
            for j in range(self.courseCol):
                self.courseEntry[i][j].delete(0, END)

        for i in range(2):
            for j in range(self.courseCol):
                self.backupCourseEntry[i][j].delete(0, END)
        '''

    def openSchedule(self):
        # pub.sendMessage("request_PPW")
        t = Toplevel(self.mainwin)
        t.wm_title("Search for Student")
        t.geometry("450x125")
        t.resizable(width=FALSE, height=FALSE)

        nameFrame = Frame(t)
        nameFrame.pack(side=TOP,anchor='w', padx=20, pady=10)

        idFrame = Frame(t)
        idFrame.pack(side=TOP, anchor='w', padx=20)

        butFrame = Frame(t)
        butFrame.pack(side=BOTTOM, anchor=CENTER, pady=10)

        label2 = Label(nameFrame, text='First name:').pack(side=LEFT)
        fnameE = ttk.Entry(nameFrame, width=10)
        fnameE.pack(side=LEFT)

        lnameE = ttk.Entry(nameFrame, width=15)
        lnameE.pack(side=RIGHT)
        label3 = Label(nameFrame, text='Last name:').pack(side=RIGHT)

        label3 = Label(idFrame, text='Student Id:').pack(side=LEFT)
        idE = ttk.Entry(idFrame, width=10)
        idE.pack(side=LEFT)

        searchB = Button(butFrame, text='Search')
        searchB.pack()

        searchB['command'] = lambda: self.searchButton(t, fnameE.get() + " " + lnameE.get(), idE.get())


    # helper function for openSchedule()
    def searchButton(self, t, name, id):
        if name != "" and id != "":
            pub.sendMessage("request_PPW", name=name, id=id)
            t.destroy()

    def createTable(self, semester, x, y):
        label1 = Label(self.innerLeftFrame, text=semester,font=('Helvetica', 15)).place(x= x, y= y-25)

        self.semesterTree = ttk.Treeview(self.innerLeftFrame, height=7)  # TIP: height is number of rows
        self.semesterTree.place(x= x, y= y)

        self.semesterTree['columns'] = ("course#", "title", "cred")

        self.semesterTree.column("#0", width=0, stretch=NO)  # important
        self.semesterTree.column("course#", anchor=CENTER, width=120)  # anchor for the data in the column
        self.semesterTree.column("title", anchor=W, width=180)
        self.semesterTree.column("cred", anchor=CENTER, width=100)

        self.semesterTree.heading("course#", text='Course Number', anchor=CENTER)  # anchor for the title of the column
        self.semesterTree.heading("title", text='Title', anchor=CENTER)
        self.semesterTree.heading("cred", text='Credit Hours', anchor=CENTER)

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
