from tkinter import *
from tkinter import ttk
# from ttkthemes import ThemedTk
from pubsub import pub  # pip install PyPubSub
# import tkinter.font as TkFont
# from PIL import ImageTk, Image  # pip install pillow


# import functionss as funct


def donothing():
    print("Something happened...")


class View:
    def __init__(self, master, majorL, minorL, subjectL):
        self.mainwin = master
        self.mainwin.title("Academic Advising Tool")
        self.mainwin.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))
        self.mainwin.minsize(width=master.winfo_screenwidth(), height=master.winfo_screenheight())
        self.mainwin.maxsize(width=master.winfo_screenwidth(), height=master.winfo_screenheight())

        self.majorsList = majorL
        self.minorsList = minorL
        self.subjectsList = subjectL

        self.TVstyle = ttk.Style()
        self.TVstyle.configure("mystyle.Treeview", font=('Helvetica', 12))
        self.TVstyle.configure("mystyle.Treeview.Heading", font=('Helvetica', 12))

        self.courseTree_counter = 0
        self.backupCourseTree_counter = 0
        self.courseTakenList_counter = 0
        self.addCourseSearchResult = []
        self.resultVar = StringVar() # for add course button

        self.fourYearCourses = []

        self.counter= 0

        self.layout()
        self.menuBar()

    def layout(self):
        self.leftFrame = Frame(self.mainwin, highlightbackground='gray', highlightthickness=1)
        self.leftFrame.pack(expand=1)
        self.leftFrame.place(relwidth=0.48, relheight=0.91, relx=0.01, rely=0.02)

        self.rightFrame = Frame(self.mainwin, highlightbackground='gray', highlightthickness=1)
        self.rightFrame.pack(expand=1)
        self.rightFrame.place(relwidth=0.48, relheight=0.91, relx=0.5, rely=0.02)

        self.courseTakenListFrame = Frame(self.mainwin, highlightbackground='gray', highlightthickness=1)
        self.courseTakenListFrame.pack(expand=1)
        self.courseTakenListFrame.place(relwidth=0.48, relheight=0.91, relx=0.01, rely=0.02)

        self.courseTakenListFrame.place_forget() # hide frame

        self.FourYearPlan()
        self.planningWorksheet_layout()
        self.courseTakenList_layout()

    def FourYearPlan(self):
        # ============================ Scroll Bar ============================
        canvas = Canvas(self.leftFrame)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)

        scrollbar = ttk.Scrollbar(self.leftFrame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self.innerLeftFrame = Frame(canvas)
        self.innerLeftFrame.pack(expand=1)
        canvas.create_window((0, 0), window=self.innerLeftFrame, anchor=NW)

        # ============================ title ============================
        ProgPlanTitleFrame=Frame(self.innerLeftFrame, width=900, height=50)
        ProgPlanTitleFrame.pack(expand=1)

        ProgPlanTitle = ttk.Label(ProgPlanTitleFrame, text="Four Year Plan", anchor=CENTER,
                                  font=('Helvetica', 19))
        ProgPlanTitle.pack(expand=1)
        ProgPlanTitle.place(x=360, y=20)

        # ============================ Student Name and ID ============================

        nameIDFrame = Frame(self.innerLeftFrame, width=900, height=50)
        nameIDFrame.pack(expand=1)

        nameLabel = Label(nameIDFrame, text='Name:')
        nameLabel.pack(side=LEFT, expand=1)
        nameLabel.place(x=181, y=20)

        self.name2Entry = ttk.Entry(nameIDFrame)
        self.name2Entry.pack(side=LEFT, expand=1)
        self.name2Entry.place(x=230, y=20)

        idLabel = Label(nameIDFrame, text='ID Number:')
        idLabel.pack(side= RIGHT, expand=1)
        idLabel.place(x=490, y=20)

        self.id2Entry = ttk.Entry(nameIDFrame, width=8)
        self.id2Entry.pack(side=RIGHT, expand=1)
        self.id2Entry.place(x=570, y=20)

        # ====================== memo ========================
        policyFrame = ttk.LabelFrame(self.innerLeftFrame, height=200, width=700, text='University Policy:')
        policyFrame.pack()

        self.policyMemoEntry = Text(policyFrame, width=90, height=10)
        self.policyMemoEntry.pack()

        # ============================ Semester Tables ============================
        self.semesterFrame = Frame(self.innerLeftFrame, width=900, height=2000)
        self.semesterFrame.pack(expand=1)

        self.yearCounter=1
        self.semesterCounter=1
        self.yPos=50
        semTable = []

        semTable.append(self.createTable("Fall 2020", 15, self.yPos))
        semTable.append(self.createTable("Spring 2021", 455, self.yPos))
        self.yPos = self.yPos + 220
        semTable.append(self.createTable("Fall 2021", 15, self.yPos))
        semTable.append(self.createTable("Spring 2022", 455, self.yPos))
        self.yPos = self.yPos + 220
        semTable.append(self.createTable("Fall 2022", 15, self.yPos))
        semTable.append(self.createTable("Spring 2023", 455, self.yPos))
        self.yPos = self.yPos + 220
        semTable.append(self.createTable("Fall 2023", 15, self.yPos))
        semTable.append(self.createTable("Spring 2024", 455, self.yPos))
        self.yPos = self.yPos + 220
        # when inserting 'iid' needs to be different
        '''
        for c in arg3:
            semTable[0].self.courseTree.insert(parent='', index='end', iid=self.courseTree_counter, text="", values=(c[0],c[1],c[2],c[3]))
            self.courseTree_counter += 1
        '''

        # ============================ Add Semester Table Button ============================
        self.addSemesterBtn = Button(self.semesterFrame, text="Add a semester")
        self.addSemesterBtn.pack()
        self.addSemesterBtn.place(x=120, y=950)
        self.addSemesterBtn['command'] = lambda: self.createSemesterBtn("Extra Semester")

    def planningWorksheet_layout(self):
        # outer most blank frames left & right
        width = self.mainwin.winfo_screenwidth()
        height = self.mainwin.winfo_screenheight()
        AspectRatio = width/height

        if AspectRatio == 16/10:
            blank1 = Frame(self.rightFrame, width=50).grid(column=0, row=0, rowspan=15, sticky=(N,E,S,W))
            #blank2 = Frame(self.rightFrame, width=50).grid(column=5, row=0, rowspan=15, sticky=(N,E,S,W))
        elif AspectRatio == 16/9:
            blank1 = Frame(self.rightFrame, width=190).grid(column=0, row=0,rowspan=15,sticky=(N, E, S, W))
            #blank2 = Frame(self.rightFrame, width=190).grid(column=5, row=0, rowspan=15,sticky=(N, E, S, W))
        elif AspectRatio == 4/3:
            blank1 = Frame(self.rightFrame, width=200).grid(column=0, row=0,rowspan=15,sticky=(N, E, S, W))
            #blank2 = Frame(self.rightFrame, width=160).grid(column=5, row=0, rowspan=15,sticky=(N, E, S, W))
        elif AspectRatio == 3/2:
            blank1 = Frame(self.rightFrame, width=160).grid(column=0, row=0,rowspan=15,sticky=(N, E, S, W))
            #blank2 = Frame(self.rightFrame, width=160).grid(column=5, row=0, rowspan=15,sticky=(N, E, S, W))
        else:
            blank1 = Frame(self.rightFrame, width=50).grid(column=0, row=0, rowspan=15, sticky=(N, E, S, W))
            #blank2 = Frame(self.rightFrame, width=50).grid(column=5, row=0, rowspan=15, sticky=(N, E, S, W))

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
        ProgPlanTitle.grid(row=0, column=2, columnspan=3, pady=8)

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

        self.idEntry = ttk.Entry(idFrame, width=8, justify=CENTER)
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

        self.enrlDateEntry = ttk.Entry(enrlDateFrame, width=8, justify=CENTER)
        self.enrlDateEntry.pack()

        # ============================ Course table ============================
        courseTableFrame = Frame(self.rightFrame)
        courseTableFrame.grid(row=12, column=1, columnspan=4)

        self.courseTree = ttk.Treeview(courseTableFrame, height=7, style="mystyle.Treeview") # TIP: height is number of rows
        self.courseTree.pack()

        self.courseTree['columns'] = ("course#", "title", "cred", "gen/elect")

        self.courseTree.column("#0", width=0, stretch=NO)   # important
        self.courseTree.column("course#", anchor=CENTER, width=80) # anchor for the data in the column
        self.courseTree.column("title", anchor=CENTER, width=295)
        self.courseTree.column("cred", anchor=CENTER, width=25)
        self.courseTree.column("gen/elect", anchor=CENTER, width=100)

        self.courseTree.heading("course#", text='Course #', anchor=CENTER) # anchor for the title of the column
        self.courseTree.heading("title", text='Title', anchor=CENTER)
        self.courseTree.heading("cred", text='CH', anchor=CENTER)
        self.courseTree.heading("gen/elect", text='Gen ed/Elect', anchor=CENTER)

        # ===================== backup course ===================
        backupCourseFrame = Frame(self.rightFrame)
        backupCourseFrame.grid(row=13, column=1, columnspan=4)

        backuplabel = Label(backupCourseFrame, text="Back-up Courses").pack(anchor=CENTER)

        self.backupCourseTree = ttk.Treeview(backupCourseFrame, height=2, style="mystyle.Treeview")
        self.backupCourseTree.pack()

        self.backupCourseTree['columns'] = ("course#", "title", "cred", "gen/elect")

        self.backupCourseTree.column("#0", width=0, stretch=NO)
        self.backupCourseTree.column("course#", anchor=CENTER, width=80)
        self.backupCourseTree.column("title", anchor=CENTER, width=295)
        self.backupCourseTree.column("cred", anchor=CENTER, width=25)
        self.backupCourseTree.column("gen/elect", anchor=CENTER, width=100)

        self.backupCourseTree.heading("course#", text='Course #', anchor=CENTER)  # anchor for the title of the column
        self.backupCourseTree.heading("title", text='Title', anchor=CENTER)
        self.backupCourseTree.heading("cred", text='CH', anchor=CENTER)
        self.backupCourseTree.heading("gen/elect", text='Gen ed/Elect', anchor=CENTER)

        # ====================== memo ========================
        memoFrame = ttk.LabelFrame(self.rightFrame, text='Memo:')
        memoFrame.grid(row=15, column=2, columnspan=2)

        self.memoEntry = Text(memoFrame, width=50, height=5)
        self.memoEntry.pack()

        # ===================== add remove course ==================
        coursebuttonFrame = Frame(self.rightFrame)
        # courseLabelFrame.grid(row=17, column=1, columnspan=3)
        coursebuttonFrame.grid(row=12, column=5, padx=20)

        addcoursebutton = ttk.Button(coursebuttonFrame, text="Add", command=self.planningWorksheet_addCourseButton)
        addcoursebutton.pack(side=TOP)

        rmcoursebutton = ttk.Button(coursebuttonFrame, text="Remove", command=self.planningWorksheet_delCourseButton)
        rmcoursebutton.pack(side=BOTTOM)

        # backup course
        bcoursebuttonFrame = Frame(self.rightFrame)
        bcoursebuttonFrame.grid(row=13, column=5, padx=20)

        addbackupbutton = ttk.Button(bcoursebuttonFrame, text="Add", command=self.planningWorksheet_addBackupCourseButton)
        addbackupbutton.pack(side=TOP)

        rmbackupbutton = ttk.Button(bcoursebuttonFrame, text="Remove", command=self.planningWorksheet_delBackupCourseButton)
        rmbackupbutton.pack(side=TOP)

    def planningWorksheet_addCourseButton(self):
        t = Toplevel(self.mainwin)
        t.wm_title("Search for Course")
        t.geometry("450x125")
        t.resizable(width=FALSE, height=FALSE)

        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')

        def courseSearch(e):
            course = entry.get()
            if len(course) > 7:
                if len(course.split()[1]) == 3:
                    pub.sendMessage("request_course#", sub=course.split()[0], cat=course.split()[1])
                    self.resultVar.set(
                        self.addCourseSearchResult[0] + " " + self.addCourseSearchResult[1] + " " * 3 +
                        self.addCourseSearchResult[2] + " " * 3 +
                        self.addCourseSearchResult[3])
                else:
                    self.resultVar.set("")
            else:
                self.resultVar.set("")

        def addCourse():
            self.courseTree.insert(parent='', index='end', iid=self.courseTree_counter, text="",
                                   values=(self.addCourseSearchResult[0] + self.addCourseSearchResult[1],
                                           self.addCourseSearchResult[2],
                                           int(float(self.addCourseSearchResult[3])),
                                           genEntry.get()))
            self.courseTree_counter += 1
            genEntry.delete(0, END)

            prevcred = self.enrollCredVar.get()
            self.enrollCredVar.set(prevcred + int(float(self.addCourseSearchResult[3])))

        f1 = Frame(t)
        f1.pack(anchor=CENTER, pady=5)

        l1 = Label(f1, text="Course Number:").pack(side=LEFT)
        entry = ttk.Entry(f1, width=10, justify=CENTER)
        entry.pack(side=LEFT)

        entry.bind('<KeyRelease>', courseSearch) # for auto search

        # sbutton =Button(f1, text="Search")
        # sbutton.pack(side=LEFT)
        # sbutton['command'] = lambda: addCourseB2(entry.get())

        rf = Frame(t)   # result frame
        rf.pack(anchor=CENTER)

        resultEntry = ttk.Entry(rf, textvariable = self.resultVar, state=DISABLED, justify=CENTER, width=50)
        resultEntry.pack(side=TOP)

        gf = Frame(t)   # gen frame
        gf.pack(anchor=CENTER)

        l2 = Label(gf, text="gen ed/elect:").pack(side=LEFT, anchor=NW)

        genEntry = ttk.Entry(gf)
        genEntry.pack(side=TOP)

        addButton = Button(gf, text="Add", command=addCourse)
        addButton.pack(side=TOP)

    def planningWorksheet_delCourseButton(self):
        for course in self.courseTree.selection():
            prevcred = self.enrollCredVar.get()
            self.enrollCredVar.set(prevcred -  int(float(self.courseTree.item(course)['values'][2])) )

            self.courseTree.delete(course)
            self.courseTree_counter -= 1

    def planningWorksheet_addBackupCourseButton(self):
        t = Toplevel(self.mainwin)
        t.wm_title("Search for Backup Course")
        t.geometry("450x125")
        t.resizable(width=FALSE, height=FALSE)

        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')

        def courseSearch(e):
            course = entry.get()
            if len(course) > 7:
                if len(course.split()[1]) == 3:
                    pub.sendMessage("request_course#", sub=course.split()[0], cat=course.split()[1])
                    self.resultVar.set(self.addCourseSearchResult[0] + " " + self.addCourseSearchResult[1] + " " * 3 +
                                       self.addCourseSearchResult[2] + " " * 3 +
                                       self.addCourseSearchResult[3])
                else:
                    self.resultVar.set("")
            else:
                self.resultVar.set("")

        def addCourse():
            self.backupCourseTree.insert(parent='', index='end', iid=self.backupCourseTree_counter, text="",
                                   values=(self.addCourseSearchResult[0] + self.addCourseSearchResult[1],
                                           self.addCourseSearchResult[2],
                                           int(float(self.addCourseSearchResult[3])),
                                           genEntry.get()))
            self.backupCourseTree_counter += 1
            genEntry.delete(0, END)

            prevcred = self.enrollCredVar.get()
            self.enrollCredVar.set(prevcred + int(float(self.addCourseSearchResult[3])))

        f1 = Frame(t)
        f1.pack(anchor=CENTER, pady=5)

        l1 = Label(f1, text="Course Number:").pack(side=LEFT)
        entry = ttk.Entry(f1, width=10, justify=CENTER)
        entry.pack(side=LEFT)

        entry.bind('<KeyRelease>', courseSearch) # for auto search

        rf = Frame(t)   # result frame
        rf.pack(anchor=CENTER)

        resultEntry = ttk.Entry(rf, textvariable = self.resultVar, state=DISABLED, justify=CENTER, width=50)
        resultEntry.pack(side=TOP)

        gf = Frame(t)   # gen frame
        gf.pack(anchor=CENTER)

        l2 = Label(gf, text="gen ed/elect:").pack(side=LEFT, anchor=NW)

        genEntry = ttk.Entry(gf)
        genEntry.pack(side=TOP)

        addButton = Button(gf, text="Add", command=addCourse)
        addButton.pack(side=TOP)

    def planningWorksheet_delBackupCourseButton(self):
        for course in self.backupCourseTree.selection():
            self.backupCourseTree.delete(course)
            self.backupCourseTree_counter -= 1

    def planningWorksheet_reset(self):
        self.fourYearCourses.clear()
        self.nameEntry.delete(0, END)
        self.idEntry.delete(0, END)

        self.enrollCredVar.set(0)

        self.earnCredEntry['state'] = NORMAL
        self.earnCredEntry.delete(0, END)
        self.earnCredEntry['state'] = 'readonly'

        self.enrlDateEntry.delete(0, END)
        self.memoEntry.delete('1.0', 'end')

        for course in self.courseTree.get_children():
            self.courseTree.delete(course)
        self.courseTree_counter = 0

        for course in self.backupCourseTree.get_children():
            self.backupCourseTree.delete(course)
        self.backupCourseTree_counter = 0

    def planningWorksheet_fill(self, obj, tcred, courses, numbCourse, bcourses, courseHist):  # (py dict, total cred, 2d course array, course size) fyp - four year plan
        # clear data in widgets
        self.planningWorksheet_reset()

        self.fourYearCourses = courseHist
        self.nameEntry.insert(END, obj['name'])
        self.idEntry.insert(END, obj['s_id'])
        self.seasonVar.set(obj['registering_for'])

        '''
        for i in range( len(self.majorsList) ):
            if obj['major'] == self.majorsList[i]:
                self.majorVar.set(self.majorsList[i])

        for i in range( len(self.minorsList) ):
            if obj['minor'] == self.minorsList[i]:
                self.minorVar.set(self.minorsList[i])
        '''

        self.earnCredEntry['state'] = NORMAL
        self.earnCredEntry.insert(END, obj['credits'])
        self.earnCredEntry['state'] = 'readonly'

        self.enrollCredVar.set(tcred)

        self.enrlDateEntry.insert(END, obj['enrll'])
        self.memoEntry.insert('1.0', obj['memo'])

        for c in courses:
            self.courseTree.insert(parent='', index='end', iid=self.courseTree_counter, text="", values=(c[0],c[1],c[2],c[3]))
            self.courseTree_counter += 1

        for c in bcourses:
            self.backupCourseTree.insert(parent='', index='end', iid=self.backupCourseTree_counter, text="", values=(c[0],c[1],c[2],c[3]))
            self.backupCourseTree_counter += 1

        self.courseTakenList_fill()

    def populateFYP(self, arg1):
        # delete what was previously there then insert
        self.name2Entry.delete(0, END)
        self.name2Entry.insert(END, arg1['name'])

        self.id2Entry.delete(0, END)
        self.id2Entry.insert(END, arg1['s_id'])

        self.policyMemoEntry.delete('1.0', 'end')
        self.policyMemoEntry.insert('1.0', arg1['memo'])

    def courseTakenList_layout(self):
        label = Label(self.courseTakenListFrame, text="Course Taken List", font=('Helvetica', 19))
        label.pack(anchor=CENTER, side=TOP, pady=20)

        self.courseTakenListTree = ttk.Treeview(self.courseTakenListFrame, show="tree", height=38, style="mystyle.Treeview")
        # self.courseTakenListTree.pack(side=TOP, padx=50, pady=10, fill=X)

        self.courseTakenListTree.column("#0")

        for subj in self.subjectsList:
            self.courseTakenListTree.insert(parent='', index='end', iid=self.courseTakenList_counter, text=str(subj))
            self.courseTakenList_counter += 1

    def courseTakenList_reset(self):
        self.courseTakenListTree.pack_forget()
        for subj in self.courseTakenListTree.get_children():
            self.courseTakenListTree.delete(subj)
        self.courseTakenList_counter = 0

        for subj in self.subjectsList:
            self.courseTakenListTree.insert(parent='', index='end', iid=self.courseTakenList_counter, text=str(subj))
            self.courseTakenList_counter += 1

    def courseTakenList_fill(self):
        self.courseTakenList_reset()
        self.courseTakenListTree.pack(side=TOP, padx=50, pady=10, fill=X)

        for sem in self.fourYearCourses:
            for course in sem:
                for id in self.courseTakenListTree.get_children():
                    if course[1] == self.courseTakenListTree.item(id)['text']:
                        name = str(course[1] + " " + course[2] + " "*5 + course[3])
                        self.courseTakenListTree.insert(parent=str(id), index='end', iid=self.courseTakenList_counter, text=name)
                        self.courseTakenList_counter += 1

        for id in self.courseTakenListTree.get_children():
            if not self.courseTakenListTree.get_children(id):
                self.courseTakenListTree.delete(id)

    def menuBar(self):
        menu = Menu(self.mainwin, tearoff=0)
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

    def newSchedule(self):
        self.planningWorksheet_reset()
        self.courseTakenList_reset()

    def openSchedule(self):
        t = Toplevel(self.mainwin)
        t.wm_title("Search for Student")
        t.geometry("450x125")
        t.resizable(width=FALSE, height=FALSE)

        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')

        def openScheduleSearchButton():
            name = fnameE.get() + " " + lnameE.get()
            id = idE.get()
            if name != "" and id != "":
                pub.sendMessage("request_PPW", name=name, id=int(id))
                t.destroy()

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

        searchB = Button(butFrame, text='Search', command=openScheduleSearchButton)
        searchB.pack()

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

    def loadMenu(self, major):
        major.add_command(label='Four Year Plan', command=self.showFourYearPlan)
        major.add_command(label='Course Taken List', command=self.showCourseTakenList)
        major.add_separator()
        major.add_command(label='Major Checklist')
        major.add_command(label='Minor Checklist')

    def showFourYearPlan(self):
        self.courseTakenListFrame.place_forget()
        self.leftFrame.place(relwidth=0.48, relheight=0.91, relx=0.01, rely=0.02)

    def showCourseTakenList(self):
        self.leftFrame.place_forget()
        self.courseTakenListFrame.place(relwidth=0.48, relheight=0.91, relx=0.01, rely=0.02)

    # data base menu dropdown
    def DataBaseMenu(self, DB):
        DB.add_command(label='Current Semester Course')
        DB.add_separator()
        DB.add_command(label='Add/Remove a Department')
        DB.add_command(label='Add/remove a Major')
        DB.add_command(label='Add/Remove a minor')

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

    def createTable(self, semester, x, y):
        if self.semesterCounter % 2 != 0:
            self.yearCounter += 1

        semesterLabel = Label(self.semesterFrame, text=semester, font=('Helvetica', 15))
        semesterLabel.pack(expand=1)
        semesterLabel.place(x=x, y=y-25)

        self.semesterTree = ttk.Treeview(self.semesterFrame, height=7)  # TIP: height is number of rows
        self.semesterTree.pack(expand=1)
        self.semesterTree.place(x=x, y=y)

        self.semesterTree['columns'] = ("course#", "title", "cred")

        self.semesterTree.column("#0", width=0, stretch=NO)  # important
        self.semesterTree.column("course#", anchor=CENTER, width=75)  # anchor for the data in the column
        self.semesterTree.column("title", anchor=W, width=295)
        self.semesterTree.column("cred", anchor=CENTER, width=62)
        # self.semesterTree.column("taken", anchor=CENTER, width=30)

        self.semesterTree.heading("course#", text='Course #', anchor=CENTER)  # anchor for the title of the column
        self.semesterTree.heading("title", text='Title', anchor=CENTER)
        self.semesterTree.heading("cred", text='Crd. Hr.', anchor=CENTER)
        # self.semesterTree.heading("taken", text='Cls. Taken', anchor=CENTER)

    def createSemesterBtn(self, semester):
        if self.counter == 1:
            self.createTable(semester, 455, self.yPos)
            self.yPos = self.yPos + 220
            self.addSemesterBtn.place(x=15, y=self.yPos)
            self.counter=0
        else:
            self.createTable(semester, 15, self.yPos)
            self.addSemesterBtn.place(x=455, y=self.yPos)
            self.counter=1