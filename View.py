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

        self.courseTree_counter = 0
        self.backupCourseTree_counter = 0

        self.addCourseSearchResult = []

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
        if self.mainwin.winfo_screenwidth() == 1920:
            blank1 = Frame(self.leftFrame, width=self.mainwin.winfo_screenwidth() / 10).grid(column=0, row=0,
                                                                                              rowspan=30,
                                                                                              sticky=(N, E, S, W))
            blank2 = Frame(self.leftFrame, width=self.mainwin.winfo_screenwidth() / 10).grid(column=5, row=0,
                                                                                              rowspan=30,
                                                                                              sticky=(N, E, S, W))
        elif self.mainwin.winfo_screenwidth() == 1600:
            blank1 = Frame(self.leftFrame, width=160).grid(column=0, row=0, rowspan=30, sticky=(N, E, S, W))
            blank2 = Frame(self.leftFrame, width=160).grid(column=5, row=0, rowspan=30, sticky=(N, E, S, W))
        else:
            blank1 = Frame(self.leftFrame, width=50).grid(column=0, row=0, rowspan=30, sticky=(N, E, S, W))
            blank2 = Frame(self.leftFrame, width=50).grid(column=5, row=0, rowspan=30, sticky=(N, E, S, W))

        h = 22
        '''
        for i in range(30):
            for j in range(30):
                blank = Frame(self.leftFrame).grid(row=i, column=j)


        # ============================ title ============================
        FourYearTitle = ttk.Label(self.leftFrame, text="Computer Science", anchor=CENTER,
                                  font=('Helvetica', 19))
        FourYearTitle.grid(row=2, column=0, columnspan=2)

        # ============================ Student Name ============================
        nameFrame = Frame(self.leftFrame)
        nameFrame.grid(row=4, column=1, columnspan=2)

        nameLabel = Label(nameFrame, text='Name:')
        nameLabel.pack(side=LEFT)

        self.nameEntry = ttk.Entry(nameFrame)
        self.nameEntry.pack()

        # ============================ Student ID ============================
        idFrame = Frame(self.leftFrame)
        idFrame.grid(row=4, column=4, columnspan=2)

        idLabel = Label(idFrame, text='ID Number:')
        idLabel.pack(side=LEFT)

        self.idEntry = ttk.Entry(idFrame, width=8)
        self.idEntry.pack()

        # ============================ Year Tables ============================
        self.semesterFrame = Frame(self.leftFrame, highlightbackground='gray')
        self.semesterFrame.grid(row=15, column=1, rowspan=10, columnspan=1)
        self.createTable("Semester 1: ", 5, 0)
        self.createTable("Semester 2: ", 11, 10)
        # self.createTable("Semester 3: ", 10, 0)
        # self.createTable("Semester 4: ", 10, 8)

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
        ProgPlanTitle.grid(row=0, column=2, columnspan=2)

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
        self.enrollCredVar = IntVar()
        self.enrollCredEntry = ttk.Entry(credFrame, width=3, textvariable=self.enrollCredVar, justify=CENTER)
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

        # ===================== add remove course ==================
        coursebuttonFrame = Frame(self.rightFrame)
        # courseLabelFrame.grid(row=17, column=1, columnspan=3)
        coursebuttonFrame.grid(row=12, column=5, padx=20)

        addcoursebutton = ttk.Button(coursebuttonFrame, text="Add", command=self.addCourseButton)
        addcoursebutton.pack(side=TOP)

        rmcoursebutton = ttk.Button(coursebuttonFrame, text="Remove", command=self.delCourseButton)
        rmcoursebutton.pack(side=BOTTOM)

        # backup course
        bcoursebuttonFrame = Frame(self.rightFrame)
        bcoursebuttonFrame.grid(row=13, column=5, padx=20)

        addbackupbutton = ttk.Button(bcoursebuttonFrame, text="Add")
        addbackupbutton.pack(side=TOP)

        rmbackupbutton = ttk.Button(bcoursebuttonFrame, text="Remove", command=self.delBackupCourseButton)
        rmbackupbutton.pack(side=TOP)

    def addCourseButton(self):
        t = Toplevel(self.mainwin)
        t.wm_title("Search for Course")
        t.geometry("450x125")
        t.resizable(width=FALSE, height=FALSE)

        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')

        # =========== for search ===================
        f1 = Frame(t)
        f1.pack(anchor=CENTER, pady=5)

        l1 = Label(f1, text="Course Number:").pack(side=LEFT)
        entry = ttk.Entry(f1, width=10)
        entry.pack(side=LEFT)

        sbutton =Button(f1, text="Search")
        sbutton.pack(side=LEFT)
        sbutton['command'] = lambda: self.addCourseB2(entry.get())

        # =============== for results =================
        rf = Frame(t)
        rf.pack(anchor=CENTER)

        self.resultVar = StringVar()

        resultEntry = ttk.Entry(rf, textvariable = self.resultVar, state=DISABLED, justify=CENTER, width=50)
        resultEntry.pack(side=TOP)

        # =============== add to tree view ================
        gf = Frame(t)
        gf.pack(anchor=CENTER)

        l2 = Label(gf, text="gen ed/elect:").pack(side=LEFT, anchor=NW)

        genEntry = ttk.Entry(gf)
        genEntry.pack(side=TOP)

        addbutton = Button(gf, text="Add", command=lambda: self.addCourseB3(genEntry))
        addbutton.pack(side=TOP)

    # addCourseButton helper function 1
    def addCourseB2(self, courseNumb):
        if courseNumb != "":
            pub.sendMessage("request_course#", sub=courseNumb.split()[0], cat=courseNumb.split()[1])
            self.resultVar.set( self.addCourseSearchResult[0] + " " + self.addCourseSearchResult[1] + " "*3 +
                                self.addCourseSearchResult[2] + " "*3 +
                                self.addCourseSearchResult[3])

    # addCourseButton helper function 2
    def addCourseB3(self, gen):
        self.courseTree.insert(parent='', index='end', iid=self.courseTree_counter, text="",
                               values=(self.addCourseSearchResult[0] + self.addCourseSearchResult[1],
                                       self.addCourseSearchResult[2],
                                       self.addCourseSearchResult[3],
                                       gen.get() ))
        self.courseTree_counter += 1
        gen.delete(0, END)

        prevcred = self.enrollCredVar.get()
        self.enrollCredVar.set( prevcred + int( float(self.addCourseSearchResult[3]) ) )

    def delCourseButton(self):
        for course in self.courseTree.selection():
            prevcred = self.enrollCredVar.get()
            self.enrollCredVar.set(prevcred -  int(float(self.courseTree.item(course)['values'][2])) )

            self.courseTree.delete(course)
            self.courseTree_counter -= 1

    def delBackupCourseButton(self):
        for course in self.backupCourseTree.selection():
            self.backupCourseTree.delete(course)
            self.backupCourseTree_counter -= 1

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

        self.enrollCredVar.set(arg2)
        #self.enrollCredEntry.delete(0, END)
        #self.enrollCredEntry.insert(END, arg2)

        self.enrlDateEntry.delete(0, END)
        self.enrlDateEntry.insert(END, arg1['enrll'])

        self.memoEntry.delete('1.0', 'end')
        self.memoEntry.insert('1.0', arg1['memo'])

        # when inserting 'iid' needs to be different
        for c in arg3:
            self.courseTree.insert(parent='', index='end', iid=self.courseTree_counter, text="", values=(c[0],c[1],c[2],c[3]))
            self.courseTree_counter += 1

        for c in arg5:
            self.backupCourseTree.insert(parent='', index='end', iid=self.backupCourseTree_counter, text="", values=(c[0],c[1],c[2],c[3]))
            self.backupCourseTree_counter += 1

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

        for course in self.courseTree.get_children():
            self.courseTree.delete(course)
        self.courseTree_counter = 0

        for course in self.backupCourseTree.get_children():
            self.backupCourseTree.delete(course)
        self.backupCourseTree_counter = 0

    def openSchedule(self):
        t = Toplevel(self.mainwin)
        t.wm_title("Search for Student")
        t.geometry("450x125")
        t.resizable(width=FALSE, height=FALSE)

        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')

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

        searchB['command'] = lambda: self.OPSsearchButton(t, fnameE.get() + " " + lnameE.get(), idE.get())

    # helper function for openSchedule()
    def OPSsearchButton(self, t, name, id):
        if name != "" and id != "":
            pub.sendMessage("request_PPW", name=name, id=id)
            t.destroy()

    def createTable(self, semester, row, col):
        label1 = Label(self.semesterFrame, text=semester).grid(row=row, column=col)


        self.semesterEntry = [[]]
        for i in range(4):
            self.semesterEntry.append([])
            for j in range(3):
                if j == 0:
                    self.semesterEntry[i].append(Entry(self.semesterFrame, bd=3, width=10, justify=CENTER))
                    self.semesterEntry[i][j].grid(row=row + i, column=j + col)
                elif j == 1:
                    self.semesterEntry[i].append(Entry(self.semesterFrame, bd=3, width=15, justify=CENTER))
                    self.semesterEntry[i][j].grid(row=row + i, column=j + col)
                elif j == 2:
                    self.semesterEntry[i].append(Entry(self.semesterFrame, bd=3, width=5, justify=CENTER))
                    self.semesterEntry[i][j].grid(row=row + i, column=j + col)
                else:
                    self.semesterEntry[i].append(Entry(self.semesterFrame, bd=3, width=5, justify=CENTER))
                    self.semesterEntry[i][j].grid(row=row + i, column=j + col)

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
