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

        # self.schList = schL
        self.subjectsList = subjectL
        self.majorList = majorL
        self.minorList = minorL

        # self.majorsList = majorL
        # self.minorsList = minorL

        self.TVstyle = ttk.Style()
        self.TVstyle.configure("mystyle.Treeview", font=('Helvetica', 12))
        self.TVstyle.configure("mystyle.Treeview.Heading", font=('Helvetica', 12))

        self.courseTree_counter = 0
        self.backupCourseTree_counter = 0
        self.courseTakenList_counter = 0
        self.addCourseSearchResult = []
        self.resultVar = StringVar() # for add course button

        self.courseHist = []

        # for major & minor treeview display
        self.majorTree_counter = 0
        self.minorTree_counter = 0

        self.counter = 0

        self.layout()
        self.menuBar()

    def layout(self):
        self.leftFrame = Frame(self.mainwin, highlightbackground='gray', highlightthickness=1)
        self.leftFrame.pack(expand=1)
        self.leftFrame.place(relwidth=0.58, relheight=0.91, relx=0.01, rely=0.02)

        self.rightFrame = Frame(self.mainwin, highlightbackground='gray', highlightthickness=1)
        self.rightFrame.pack(expand=1)
        self.rightFrame.place(relwidth=0.40, relheight=0.91, relx=0.6, rely=0.02)

        self.courseTakenListFrame = Frame(self.mainwin, highlightbackground='gray', highlightthickness=1)
        self.courseTakenListFrame.pack(expand=1)
        self.courseTakenListFrame.place(relwidth=0.58, relheight=0.91, relx=0.01, rely=0.02)

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
        scrollbar.place(relwidth=0.022, relheight=0.98, relx=0.98, rely=0.00)

        scrollbar2 = ttk.Scrollbar(self.leftFrame, orient=HORIZONTAL, command=canvas.xview)
        scrollbar2.pack(side=BOTTOM, fill=X)
        scrollbar2.place(relwidth=0.98, relheight=0.022, relx=0.00, rely=0.98)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.configure(xscrollcommand=scrollbar2.set)
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
        self.semesterFrame = Frame(self.innerLeftFrame, width=900, height=1375)
        self.semesterFrame.pack(expand=1)

        self.yearCounter=1
        self.semesterCounter=0
        self.yPos=50
        self.semLabel = []
        self.semTable = []
        yearCount=0

        for i in range(8):
            if self.semesterCounter % 2 == 0:
                yearCount+=1
                self.semTable.insert(i, self.createTable("Year:"+str(yearCount), 15, self.yPos))
            else:
                self.semTable.insert(i, self.createTable(" ", 455, self.yPos))

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
        elif AspectRatio == 16/9:
            blank1 = Frame(self.rightFrame, width=190).grid(column=0, row=0,rowspan=15,sticky=(N, E, S, W))
        elif AspectRatio == 4/3:
            blank1 = Frame(self.rightFrame, width=200).grid(column=0, row=0,rowspan=15,sticky=(N, E, S, W))
        elif AspectRatio == 3/2:
            blank1 = Frame(self.rightFrame, width=160).grid(column=0, row=0,rowspan=15,sticky=(N, E, S, W))
        else:
            blank1 = Frame(self.rightFrame, width=50).grid(column=0, row=0, rowspan=15, sticky=(N, E, S, W))

        pad = 12 # pady value for most frames below

        # ============================ title ============================
        ProgPlanTitle = ttk.Label(self.rightFrame, text="Program Planning Worksheet", anchor=CENTER,
                                  font=('Helvetica', 19))
        ProgPlanTitle.grid(row=0, column=1, columnspan=3, pady=pad)

        # ============================ student name ============================
        nameFrame = Frame(self.rightFrame)
        nameFrame.grid(row=2, column=1, columnspan=2, pady=pad)

        nameLabel = Label(nameFrame, text='Name:')
        nameLabel.pack(side=LEFT)

        self.nameEntry = ttk.Entry(nameFrame)
        self.nameEntry.pack()

        # ============================ student id ============================
        idFrame = Frame(self.rightFrame)
        idFrame.grid(row=2, column=3, columnspan=2, pady=pad)

        idLabel = Label(idFrame, text='ID Number:')
        idLabel.pack(side=LEFT)

        self.idEntry = ttk.Entry(idFrame, width=8, justify=CENTER)
        self.idEntry.pack()

        # ============================ season ============================
        self.seasonVar = StringVar()

        seasonFrame = Frame(self.rightFrame)
        seasonFrame.grid(row=4, column=1, columnspan=4, pady=pad)

        seasonLabel = Label(seasonFrame, text='Registering for:')
        fallRadioBtn = ttk.Radiobutton(seasonFrame, text='Fall', variable=self.seasonVar, value='Fall')
        summerRadioBtn = ttk.Radiobutton(seasonFrame, text='Summer', variable=self.seasonVar, value='Summer')
        springRadioBtn = ttk.Radiobutton(seasonFrame, text='Spring', variable=self.seasonVar, value='Spring')
        winterRadioBtn = ttk.Radiobutton(seasonFrame, text='Winter', variable=self.seasonVar, value='Winter')

        seasonLabel.grid(row=0, column=0, padx=10)
        fallRadioBtn.grid(row=0, column=1, padx=10)
        winterRadioBtn.grid(row=0, column=2, padx=10)
        springRadioBtn.grid(row=0, column=3, padx=10)
        summerRadioBtn.grid(row=0, column=4)

        # ============================ major & minor ============================
        careerFrame = Frame(self.rightFrame)
        careerFrame.grid(row=6, column=0, columnspan=5, pady=pad)

        self.majorTree = ttk.Treeview(careerFrame, height=3, style="mystyle.Treeview", selectmode='none')
        self.majorTree.pack(side=LEFT, padx=20)
        self.majorTree.column("#0", width=150, anchor=CENTER)
        self.majorTree.heading("#0", text="Majors")

        editButton = Button(careerFrame, text="Edit", command=self.editMajorMinor)
        editButton.pack(side=LEFT)

        self.minorTree = ttk.Treeview(careerFrame, height=3, style="mystyle.Treeview", selectmode='none')
        self.minorTree.pack(side=RIGHT, padx=20)
        self.minorTree.column("#0", width=150, anchor=CENTER)
        self.minorTree.heading("#0", text="Minors")


        '''' 
        schLabel = Label(careerFrame, text="School")
        majorLabel = Label(careerFrame, text="Major")
        minorLabel = Label(careerFrame, text="Minor")

        schLabel.grid(row=0, column=0)
        majorLabel.grid(row=0, column=2)
        minorLabel.grid(row=0, column=3)

        comboboxWidth = 10
        self.schCbox = ttk.Combobox(careerFrame, width=comboboxWidth, value=self.schList)
        self.majorCbox = ttk.Combobox(careerFrame, width=comboboxWidth)
        self.minorCbox = ttk.Combobox(careerFrame, width=comboboxWidth)

        self.schCbox.grid(row=1, column=0)
        filler = Label(careerFrame).grid(column=1, row=0, rowspan=2, padx=18)
        self.majorCbox.grid(row=1, column=2)
        self.minorCbox.grid(row=1, column=3)

        self.schCbox.bind("<<ComboboxSelected>>", self.getMajorMinor)
        '''
        # ============================ credits ============================
        credFrame = Frame(self.rightFrame, )
        credFrame.grid(row=8, column=1, columnspan=4, pady=pad)

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
        enrlDateFrame.grid(row=10, column=2, columnspan=2, pady=pad)

        enrlDate = Label(enrlDateFrame, text='Enrollment Date:')
        enrlDate.pack(side=LEFT)

        self.enrlDateEntry = ttk.Entry(enrlDateFrame, width=8, justify=CENTER)
        self.enrlDateEntry.pack()

        # ============================ Course table ============================
        courseTableFrame = Frame(self.rightFrame)
        courseTableFrame.grid(row=12, column=1, columnspan=4, pady=pad)

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
        backupCourseFrame.grid(row=14, column=1, columnspan=4, pady=pad)

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
        memoFrame.grid(row=16, column=2, columnspan=2, pady=pad)

        self.memoEntry = Text(memoFrame, width=50, height=5)
        self.memoEntry.pack()

        # ===================== add remove course ==================
        coursebuttonFrame = Frame(self.rightFrame)
        # courseLabelFrame.grid(row=17, column=1, columnspan=3)
        coursebuttonFrame.grid(row=13, column=2, columnspan=2)

        addcoursebutton = ttk.Button(coursebuttonFrame, text="Add", command=self.planningWorksheet_addCourseButton)
        addcoursebutton.pack(side=LEFT)

        rmcoursebutton = ttk.Button(coursebuttonFrame, text="Remove", command=self.planningWorksheet_delCourseButton)
        rmcoursebutton.pack(side=RIGHT)

        # backup course
        bcoursebuttonFrame = Frame(self.rightFrame)
        bcoursebuttonFrame.grid(row=15, column=2, columnspan=2)

        addbackupbutton = ttk.Button(bcoursebuttonFrame, text="Add", command=self.planningWorksheet_addBackupCourseButton)
        addbackupbutton.pack(side=LEFT)

        rmbackupbutton = ttk.Button(bcoursebuttonFrame, text="Remove", command=self.planningWorksheet_delBackupCourseButton)
        rmbackupbutton.pack(side=RIGHT)

    ''''
    def getMajorMinor(self, e):
        pub.sendMessage("request_major_minor", sch=self.schCbox.get() )
        self.majorCbox['value'] = self.majorList
        self.minorCbox['value'] = self.minorList
    '''

    def editMajorMinor(self):
        t = Toplevel(self.mainwin)
        t.wm_title("Major & Minor")
        t.geometry("425x250")
        t.resizable(width=FALSE, height=FALSE)
        t.attributes('-topmost', 'true')

        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')

        selection_color = "red"

        def search(e, w):
            if w == 'M':
                word = search_major.get()
                for i in range(0, len(self.majorList)):
                    mj = self.majorList[i]
                    self.majorBox.itemconfig(i, foreground="white")
                    if word == "":
                        self.majorBox.itemconfig(i, foreground="white")
                    if word.lower() == mj[0:len(word)].lower():
                        self.majorBox.see(i)
                        self.majorBox.itemconfig(i, foreground=selection_color)
            else:
                word = search_minor.get()
                for i in range(0, len(self.minorList)):
                    mn = self.minorList[i]
                    self.minorBox.itemconfig(i, foreground="white")
                    if word == "":
                        self.minorBox.itemconfig(i, foreground="white")
                    if word.lower() == mn[0:len(word)].lower():
                        self.minorBox.see(i)
                        self.minorBox.itemconfig(i, foreground=selection_color)

        majorframe = Frame(t)
        majorframe.pack(side=LEFT, padx=10, fill=Y)

        minorframe = Frame(t)
        minorframe.pack(side=RIGHT, padx=10, fill=Y)

        label1 = Label(majorframe, text="Search for Majors:").pack(side=TOP, pady=5)
        search_major = ttk.Entry(majorframe, justify=CENTER)
        search_major.pack(side=TOP)
        search_major.bind('<KeyRelease>', lambda event, w='M': search(event, w))

        label2 = Label(minorframe, text="Search for Minors:").pack(side=TOP, pady=5)
        search_minor = ttk.Entry(minorframe, justify=CENTER)
        search_minor.pack(side=TOP)
        search_minor.bind('<KeyRelease>', lambda event, w='m':search(event, w))

        majorVar = StringVar()
        majorVar.set(self.majorList)
        self.majorBox = Listbox(majorframe, selectmode=MULTIPLE, justify=CENTER, listvariable=majorVar, exportselection=False)
        # exportselection allows us to work on other listbox while not calling this binding
        self.majorBox.pack(side=TOP)
        self.majorBox.bind('<<ListboxSelect>>', lambda event:self.setMajor_treeview(event))

        minorVar = StringVar()
        minorVar.set(self.minorList)
        self.minorBox = Listbox(minorframe, selectmode=MULTIPLE, justify=CENTER, listvariable=minorVar, exportselection=False)
        self.minorBox.pack(side=TOP)
        self.minorBox.bind('<<ListboxSelect>>', lambda event: self.setMinor_treeview(event))

    def setMajor_treeview(self, e):
        # clear tree view
        for id in self.majorTree.get_children():
            self.majorTree.delete(id)
        # fill in selections from listbox
        for i in self.majorBox.curselection():
            word = self.majorList[i]
            self.majorTree.insert(parent='', index='end', iid=i, text=str(word))

    def setMinor_treeview(self, e):
        for id in self.minorTree.get_children():
            self.minorTree.delete(id)
        for i in self.minorBox.curselection():
            word = self.minorList[i]
            self.minorTree.insert(parent='', index='end', iid=i, text=str(word))

    def planningWorksheet_addCourseButton(self):
        t = Toplevel(self.mainwin)
        t.wm_title("Search for Course")
        t.geometry("450x125")
        t.resizable(width=FALSE, height=FALSE)
        t.attributes('-topmost', 'true')

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
        t.attributes('-topmost', 'true')

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
        self.courseHist.clear()
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

    def planningWorksheet_fill(self, obj, tcred, courses, numbCourse, bcourses, courseHist, fourYear, policies):  # (py dict, total cred, 2d course array, course size) fyp - four year plan
        # clear data in widgets
        self.planningWorksheet_reset()

        self.courseHist = courseHist
        self.nameEntry.insert(END, obj['name'])
        self.idEntry.insert(END, obj['s_id'])
        self.seasonVar.set(obj['registering_for'])

        # self.schCbox.set(obj['dept'])                                                     #TODO fill major & minor treeview
        # self.getMajorMinor(0) # zero is just for filler since the function is called with binding

        # self.majorCbox.set(obj['major'])
        # self.minorCbox.set(obj['minor'])

        #print(obj['major'])
        #print(obj['minor'])

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

    def fourYearPlan_fill(self, obj, tcred, courses, numbCourse, bcourses, courseHist, fourYear, policies):
        self.semTableTree_counter = 0

        # delete what was previously there then insert
        self.name2Entry.delete(0, END)
        self.name2Entry.insert(END, obj['name'])

        self.id2Entry.delete(0, END)
        self.id2Entry.insert(END, obj['s_id'])

        index = 0
        self.semTableTree_counter = 0

        for sem in fourYear:
            for course in sem:
                        self.semTable[index].insert(parent='', index='end', iid=self.semTableTree_counter,
                                             values=(course[1] + " " + course[2], course[3], course[4]))
                        self.semTableTree_counter += 1
            index += 1

        self.policyMemoEntry.delete('1.0', 'end')
        self.policyMemoEntry.insert('1.0', policies)

    def FYP_reset(self):
        self.courseHist.clear()
        self.name2Entry.delete(0, END)
        self.id2Entry.delete(0, END)

        self.policyMemoEntry.delete('1.0', 'end')
        index = 0
        length = len(self.semTable)

        while(index < len(self.semTable)):
            for course in self.semTable[index].get_children():
                self.semTable[index].delete(course)
                self.semTableTree_counter += 1
            index += 1

    def courseTakenList_layout(self):
        label = Label(self.courseTakenListFrame, text="Course Taken List", font=('Helvetica', 19))
        label.pack(anchor=CENTER, side=TOP, pady=20)

        self.courseTakenListTree = ttk.Treeview(self.courseTakenListFrame, show="tree", height=38, style="mystyle.Treeview")
        # self.courseTakenListTree.pack(side=TOP, padx=50, pady=10, fill=X)
        self.courseTakenListTree['columns'] = ("grade")
        self.courseTakenListTree.column("#0")
        self.courseTakenListTree.column("grade")

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

        for sem in self.courseHist:
            for course in sem:
                for id in self.courseTakenListTree.get_children():
                    if course[1] == self.courseTakenListTree.item(id)['text']:  # comparing subjects
                        name = str(course[1] + " " + course[2] + " "*5 + course[3])
                        self.courseTakenListTree.insert(parent=str(id), index='end', iid=self.courseTakenList_counter, text=name, values=(course[5]))
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
        schedule.add_command(label='New', command=self.newSchedule)
        schedule.add_command(label='Open...', command=self.openSchedule)
        schedule.add_separator()
        schedule.add_command(label='Save', command=self.saveSchedule)
        schedule.add_separator()
        schedule.add_command(label='Export', command=self.exportSchedule)
        schedule.add_command(label='Print', command=self.printSchedule)

    def newSchedule(self):
        self.planningWorksheet_reset()
        self.FYP_reset()
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
                # pub.sendMessage("request_FYP", name=name, id=int(id))
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

    def saveSchedule(self):
        majors, minors =  [], []
        for i in self.majorBox.curselection():
            majors.append(self.majorList[i])
        for i in self.minorBox.curselection():
            minors.append(self.minorList[i])                                            # TODO: when minor list is empty

        courses, bcourses = [], []
        for id in self.courseTree.get_children():
            courses.append(self.courseTree.item(id)['values'])
        for id in self.backupCourseTree.get_children():
            bcourses.append(self.backupCourseTree.item(id)['values'])

        pydict = {
            "name": self.nameEntry.get(),
            "s_id": self.idEntry.get(),
            #"dept": self.schCbox.get(),
            #"major": self.majorCbox.get(),
            #"minor": self.minorCbox.get(),
            "taking_course": courses,
            "backup_course": bcourses
        }
        pub.sendMessage("save_schedule", obj=pydict)

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
        self.leftFrame.place(relwidth=0.58, relheight=0.91, relx=0.01, rely=0.02)

    def showCourseTakenList(self):
        self.leftFrame.place_forget()
        self.courseTakenListFrame.place(relwidth=0.58, relheight=0.91, relx=0.01, rely=0.02)

    # data base menu dropdown
    def DataBaseMenu(self, DB):
        DB.add_command(label='Current Semester Course')
        DB.add_separator()
        DB.add_command(label='Add/Remove a School')
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
            endOfArray = len(self.semTable)
            endOfSemLabel = len(self.semLabel)

            self.semLabel.append(Label(self.semesterFrame, text=semester, font=('Helvetica', 15)))
            self.semLabel[endOfSemLabel].pack(expand=1)

            self.semTable.append(ttk.Treeview(self.semesterFrame, height=7))

            if self.semesterCounter % 2 == 0:
                self.semTable[endOfArray].pack(expand=1)
                self.semTable[endOfArray].place(x=15, y=self.yPos)
                self.semLabel[endOfSemLabel].place(x=15, y=self.yPos - 25)
            else:
                self.semTable[endOfArray].pack(expand=1)
                self.semTable[endOfArray].place(x=455, y=self.yPos)
                self.semLabel[endOfSemLabel].place(x=455, y=self.yPos - 25)
                self.yPos += 190
            self.semesterCounter += 1


            self.semTable[endOfArray]['columns']= ("course#", "title", "cred")
            self.semTable[endOfArray].column("#0", width=0, stretch=NO)  # important
            self.semTable[endOfArray].column("course#", anchor=CENTER, width=75)  # anchor for the data in the column
            self.semTable[endOfArray].column("title", anchor=W, width=295)
            self.semTable[endOfArray].column("cred", anchor=CENTER, width=62)
            # self.semesterTree.column("taken", anchor=CENTER, width=30)

            self.semTable[endOfArray].heading("course#", text='Course #', anchor=CENTER)  # anchor for the title of the column
            self.semTable[endOfArray].heading("title", text='Title', anchor=CENTER)
            self.semTable[endOfArray].heading("cred", text='Crd. Hr.', anchor=CENTER)

            return self.semTable[endOfArray]

    def createSemesterBtn(self, semester):
        if self.semesterCounter % 2 == 0:
            self.createTable(semester, 15, self.yPos)
            self.addSemesterBtn.place(x=455, y=self.yPos)
        else:
            self.createTable(semester, 455, self.yPos)
            self.addSemesterBtn.place(x=15, y=self.yPos)