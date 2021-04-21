from tkinter import *
from tkinter import ttk
# import tkinter as tk
# from ttkthemes import ThemedTk
from pubsub import pub  # pip install PyPubSub
import tkinter.font as TkFont
# from PIL import ImageTk, Image  # pip install pillow
from tkinter import messagebox


class View:
    def __init__(self, master, schL, subjectL):
        self.mainwin = master
        self.mainwin.title("Academic Advising Tool")
        self.mainwin.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))

        # self.mainwin.resizable(width=0, height=0)
        # 2560 x 1440
        self.mainwin.deiconify()

        #self.mainwin.call('tk', 'scaling', 0.75)

        self.defaultFont = TkFont.nametofont("TkDefaultFont")
        self.defaultFont.configure(family='Helvetica', size=14)

        self.TVstyle = ttk.Style()
        self.TVstyle.configure("mystyle.Treeview", font=('Helvetica', 12))
        self.TVstyle.configure("mystyle.Treeview.Heading", font=('Helvetica', 12))

        self.schList = schL
        self.subjectsList = subjectL

        self.progressRepo_counter = 0

        self.courseTree_counter = 0
        self.backupCourseTree_counter = 0
        self.courseTakenList_counter = 0
        self.addCourseSearchResult = []
        self.resultVar = StringVar()  # for add course button

        self.courseHist = []

        self.layout()
        self.menuBar()

    def layout(self):
        self.right_width = self.mainwin.winfo_screenwidth() * 0.4
        self.left_width = self.mainwin.winfo_screenwidth() - self.right_width

        # four year plan
        self.leftFrame = Frame(self.mainwin, highlightbackground='gray', highlightthickness=2, width=self.left_width)
        self.leftFrame.pack(side=LEFT, fill=Y)

        # program planning worksheet
        self.PPWFrame = Frame(self.mainwin, highlightbackground='gray', highlightthickness=2, width=self.right_width)
        self.PPWFrame.pack(side=RIGHT, fill=Y)
        self.PPWFrame.pack_propagate(0)

        self.courseTakenListFrame = Frame(self.mainwin, highlightbackground='gray', highlightthickness=2,
                                          width=self.left_width)
        self.courseTakenListFrame.pack(side=LEFT, fill=Y)
        self.courseTakenListFrame.pack_propagate(0)
        self.courseTakenListFrame.pack_forget()     # hide frame

        self.FourYearPlan()
        self.planningWorksheet_layout()
        self.courseTakenList_layout()

    def FourYearPlan(self):
        # ============================ Scroll Bar ============================
        canvas = Canvas(self.leftFrame, width=self.left_width)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)

        scrollbar = ttk.Scrollbar(self.leftFrame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        #scrollbar.place(relwidth=0.022, relheight=0.98, relx=0.98, rely=0.00)

        #scrollbar2 = ttk.Scrollbar(self.leftFrame, orient=HORIZONTAL, command=canvas.xview)
        #scrollbar2.pack(side=BOTTOM, fill=X)
        #scrollbar2.place(relwidth=0.98, relheight=0.022, relx=0.00, rely=0.98)

        canvas.configure(yscrollcommand=scrollbar.set)
        #canvas.configure(xscrollcommand=scrollbar2.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.innerLeftFrame = Frame(canvas)
        self.innerLeftFrame.pack(expand=1)
        canvas.create_window((0, 0), window=self.innerLeftFrame, anchor=NW, width=self.left_width)

        # ============================ title ============================
        ProgPlanTitleFrame = Frame(self.innerLeftFrame, width=self.left_width, height=50)
        ProgPlanTitleFrame.pack(expand=1)

        ProgPlanTitle = ttk.Label(ProgPlanTitleFrame, text="Four Year Plan", anchor=CENTER,
                                  font=('Helvetica', 19))
        ProgPlanTitle.pack(expand=1)
        ProgPlanTitle.place(x=360, y=20)

        # ============================ Student Name and ID ============================

        nameIDFrame = Frame(self.innerLeftFrame, width=self.left_width, height=50)
        nameIDFrame.pack(expand=1)

        nameLabel = Label(nameIDFrame, text='Name:')
        nameLabel.pack(side=LEFT, expand=1)
        nameLabel.place(x=181, y=20)

        self.name2Entry = ttk.Entry(nameIDFrame)
        self.name2Entry.pack(side=LEFT, expand=1)
        self.name2Entry.place(x=230, y=20)

        idLabel = Label(nameIDFrame, text='ID Number:')
        idLabel.pack(side=RIGHT, expand=1)
        idLabel.place(x=490, y=20)

        self.id2Entry = ttk.Entry(nameIDFrame, width=8)
        self.id2Entry.pack(side=RIGHT, expand=1)
        self.id2Entry.place(x=570, y=20)

        # ============================ Memo ============================
        policyFrame = ttk.LabelFrame(self.innerLeftFrame, height=200, width=self.left_width, text='University Policy:')
        policyFrame.pack(pady=30)

        self.policyMemoEntry = Text(policyFrame, width=90, height=10)
        self.policyMemoEntry.pack()

        # ============================ Four Year Tabs and Progress Report ============================
        self.tab_parent = ttk.Notebook(self.innerLeftFrame)

        self.progressRepoFrame = Frame(self.tab_parent, width=self.left_width)
        self.progressRepoFrame.pack(fill='both')

        """"
        self.addProgRepoBtn = Button(self.progressRepoFrame, text="Add", command=self.FYP_addCourseButton)
        self.addProgRepoBtn.pack()
        self.addProgRepoBtn.place(x=696, y=10)

        self.removeProgRepoBtn = Button(self.progressRepoFrame, text="Remove", command=self.FYP_delCourseButton)
        self.removeProgRepoBtn.pack()
        self.removeProgRepoBtn.place(x=755, y=10)
        """

        self.tab_parent.bind('<ButtonRelease>', self.updatePolicy)
        self.tab_parent.pack(expand=1, fill=X, pady=30, ipady=5)

        self.yearCounter2 = 1
        yPos2 = 50
        self.progLabel = []
        self.progTable = []
        yearCount2 = 0

        self.createTable(self.progressRepoFrame, self.progLabel, self.progTable)

        # ============================ Semester Tables ============================
        self.semesterFrame = Frame(self.tab_parent, width=self.left_width)
        self.semesterFrame.pack(fill='both')
        # self.semesterFrame.place(x=50, y=500)

        # Adding to notebook for tab functionality
        self.tab_parent.add(self.progressRepoFrame, text="Progress Report")
        self.tab_parent.add(self.semesterFrame, text="Four Year Plan")

        self.yearCounter = 1
        semesterCounter = 0
        yPos = 50
        self.semLabel = []
        self.semTable = []
        yearCount = 0

        self.createTable(self.semesterFrame, self.semLabel, self.semTable)

        # ============================ Add Semester Table Button ============================
        """"
        self.addSemesterBtn = Button(self.semesterFrame, text="Add a semester")
        self.addSemesterBtn.pack()
        self.addSemesterBtn.place(x=120, y=950)
        self.temp = semesterCounter
        self.tempY = yPos
        self.addSemesterBtn['command'] = lambda: self.createSemesterBtn("Extra Semester", self.tempY, self.semTable,
                                                                        self.semLabel, self.semesterFrame, self.temp)
                                                                        """

    def createTable(self, frame, labels, tables):
        # column configure
        for i in range(2):
            frame.columnconfigure(i, weight=1)

        # define treeviews and labels
        for i in range(8):
            tables.append(ttk.Treeview(frame, height=7, style="mystyle.Treeview"))

            tables[i]['columns'] = ("course#", "title", "cred")
            tables[i].column("#0", width=0, stretch=NO)
            tables[i].column("course#", anchor=CENTER, width=75)
            tables[i].column("title", anchor=W, width=295)
            tables[i].column("cred", anchor=CENTER, width=25)
            # tables[i].column("taken", anchor=CENTER, width=30)

            tables[i].heading("course#", text='Course #', anchor=CENTER)
            tables[i].heading("title", text='Title', anchor=CENTER)
            tables[i].heading("cred", text='CR', anchor=CENTER)

            if i < 8 / 2:
                labels.append(Label(frame, text="Year " + str(i + 1), font=('Helvetica', 15)))

        # grid labels
        for i in range(4):
            labels[i].grid(column=0, row=2 * i, columnspan=2, sticky=W, padx=5)

        # grid treeviews
        for i in range(0, 8 - 1, 2):
            tables[i].grid(column=0, row=i + 1)
            tables[i + 1].grid(column=1, row=i + 1)

    def planningWorksheet_layout(self):
        self.rightFrame = Frame(self.PPWFrame)
        self.rightFrame.pack(fill=BOTH)

        for i in range(4):
            self.rightFrame.columnconfigure(i, weight=1)

        pad = 10  # pady value for most frames below

        # ============================ title ============================
        ProgPlanTitle = ttk.Label(self.rightFrame, text="Program Planning Worksheet", anchor=CENTER,
                                  font=('Helvetica', 19))
        ProgPlanTitle.grid(row=0, column=0, columnspan=4, pady=pad)

        # ============================ student name ============================
        nameFrame = Frame(self.rightFrame)
        nameFrame.grid(row=2, column=0, columnspan=2, pady=pad)

        nameLabel = Label(nameFrame, text='Name:')
        nameLabel.pack(side=LEFT)

        self.nameEntry = ttk.Entry(nameFrame)
        self.nameEntry.pack()

        # ============================ student id ============================
        idFrame = Frame(self.rightFrame)
        idFrame.grid(row=2, column=2, columnspan=2, pady=pad)

        idLabel = Label(idFrame, text='ID Number:')
        idLabel.pack(side=LEFT)

        self.idEntry = ttk.Entry(idFrame, width=8, justify=CENTER)
        self.idEntry.pack()

        # ============================ season ============================
        seasonFrame = Frame(self.rightFrame)
        seasonFrame.grid(row=4, column=0, columnspan=4, pady=pad)

        self.seasonVar = StringVar()

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
        careerFrame.grid(row=6, column=0, columnspan=4, pady=pad)

        self.majorTree = ttk.Treeview(careerFrame, height=3, style="mystyle.Treeview", selectmode='none')
        self.majorTree.pack(side=LEFT, padx=30)
        self.majorTree.column("#0", width=150)
        self.majorTree.heading("#0", text="Majors")

        self.editCareerButton = ttk.Button(careerFrame, text="Edit", command=self.editMajorMinor)
        self.editCareerButton.pack(side=LEFT)

        self.minorTree = ttk.Treeview(careerFrame, height=3, style="mystyle.Treeview", selectmode='none')
        self.minorTree.pack(side=RIGHT, padx=30)
        self.minorTree.column("#0", width=150)
        self.minorTree.heading("#0", text="Minors")

        # ============================ credits ============================
        credFrame = Frame(self.rightFrame)
        credFrame.grid(row=8, column=0, columnspan=4, pady=pad)

        credFrameL = Frame(credFrame)
        credFrameL.pack(side=LEFT, padx=15)

        credFrameR = Frame(credFrame)
        credFrameR.pack(side=RIGHT, padx=15)

        credLabel1 = Label(credFrameL, text='Earned:')
        self.earnCredEntry = ttk.Entry(credFrameL, width=3, justify=CENTER, state=DISABLED)
        credLabel2 = Label(credFrameL, text='credits.')

        credLabel1.grid(row=0, column=0)
        self.earnCredEntry.grid(row=0, column=1)
        credLabel2.grid(row=0, column=2)

        credLabel3 = Label(credFrameR, text='Currently Enrolled in.')
        self.enrollCredVar = IntVar()
        self.enrollCredEntry = ttk.Entry(credFrameR, width=3, textvariable=self.enrollCredVar, justify=CENTER)
        credLabel4 = Label(credFrameR, text='Credits')

        credLabel4.grid(row=0, column=0)
        self.enrollCredEntry.grid(row=0, column=1)
        credLabel3.grid(row=0, column=2)

        # ====================== Enrollment Date ========================
        enrlDateFrame = ttk.Frame(self.rightFrame)
        enrlDateFrame.grid(row=10, column=0, columnspan=4, pady=pad)

        enrlDate = Label(enrlDateFrame, text='Enrollment Date:')
        enrlDate.pack(side=LEFT)

        self.enrlDateEntry = ttk.Entry(enrlDateFrame, width=8, justify=CENTER)
        self.enrlDateEntry.pack()

        # ============================ Course table ============================
        courseTableFrame = Frame(self.rightFrame)
        courseTableFrame.grid(row=12, column=0, columnspan=4, pady=pad)

        self.courseTree = ttk.Treeview(courseTableFrame, height=7, style="mystyle.Treeview")
        # height is number of rows
        self.courseTree.pack()

        self.courseTree['columns'] = ("course#", "title", "cred", "gen/elect")

        self.courseTree.column("#0", width=0, stretch=NO)  # important
        self.courseTree.column("course#", anchor=CENTER, width=80)  # anchor for the data in the column
        self.courseTree.column("title", anchor=CENTER, width=295)
        self.courseTree.column("cred", anchor=CENTER, width=25)
        self.courseTree.column("gen/elect", anchor=CENTER, width=80)

        self.courseTree.heading("course#", text='Course #', anchor=CENTER)  # anchor for the title of the column
        self.courseTree.heading("title", text='Title', anchor=CENTER)
        self.courseTree.heading("cred", text='CR', anchor=CENTER)
        self.courseTree.heading("gen/elect", text='Gen ed/Elect', anchor=CENTER)

        # ===================== backup course ===================
        backupCourseFrame = Frame(self.rightFrame)
        backupCourseFrame.grid(row=14, column=0, columnspan=4, pady=pad)

        backuplabel = Label(backupCourseFrame, text="Back-up Courses").pack(anchor=CENTER)

        self.backupCourseTree = ttk.Treeview(backupCourseFrame, height=2, style="mystyle.Treeview")
        self.backupCourseTree.pack()

        self.backupCourseTree['columns'] = ("course#", "title", "cred", "gen/elect")

        self.backupCourseTree.column("#0", width=0, stretch=NO)
        self.backupCourseTree.column("course#", anchor=CENTER, width=80)
        self.backupCourseTree.column("title", anchor=CENTER, width=295)
        self.backupCourseTree.column("cred", anchor=CENTER, width=25)
        self.backupCourseTree.column("gen/elect", anchor=CENTER, width=80)

        self.backupCourseTree.heading("course#", text='Course #', anchor=CENTER)  # anchor for the title of the column
        self.backupCourseTree.heading("title", text='Title', anchor=CENTER)
        self.backupCourseTree.heading("cred", text='CR', anchor=CENTER)
        self.backupCourseTree.heading("gen/elect", text='Gen ed/Elect', anchor=CENTER)

        # ====================== memo ========================
        memoFrame = ttk.LabelFrame(self.rightFrame, text='Memo:')
        memoFrame.grid(row=16, column=0, columnspan=4, pady=pad)

        self.memoEntry = Text(memoFrame, width=50, height=5)
        self.memoEntry.pack()

        # ===================== add remove course ==================
        coursebuttonFrame = Frame(self.rightFrame)
        coursebuttonFrame.grid(row=13, column=0, columnspan=4)

        self.addCourseButton = ttk.Button(coursebuttonFrame, text="Add", command=self.planningWorksheet_addCourseButton)
        self.addCourseButton.pack(side=LEFT)

        rmCourseButton = ttk.Button(coursebuttonFrame, text="Remove", command=self.planningWorksheet_delCourseButton)
        rmCourseButton.pack(side=RIGHT)

        # backup course
        bcoursebuttonFrame = Frame(self.rightFrame)
        bcoursebuttonFrame.grid(row=15, column=0, columnspan=4)

        self.addBackupButton = ttk.Button(bcoursebuttonFrame, text="Add",
                                          command=self.planningWorksheet_addBackupCourseButton)
        self.addBackupButton.pack(side=LEFT)

        rmBackupButton = ttk.Button(bcoursebuttonFrame, text="Remove",
                                    command=self.planningWorksheet_delBackupCourseButton)
        rmBackupButton.pack(side=RIGHT)

    # Popup window for editing student major and minor from program planning sheet
    # called from button command
    def editMajorMinor(self):
        t = Toplevel(self.mainwin)
        t.wm_title("Major & Minor")
        t.geometry("425x425")
        t.resizable(width=FALSE, height=FALSE)
        t.transient(self.mainwin)
        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')

        def close(e):
            self.editCareerButton.configure(state=NORMAL)
        t.bind('<Destroy>', close)
        self.editCareerButton.configure(state=DISABLED)

        # insert selected major into separate listbox
        def majorSelection(e):
            i = self.majorBox.curselection()
            self.selected_major_Box.insert(END, self.majorBox.get(i))

        def removeMajor():
            i = self.selected_major_Box.curselection()
            msg = "Do you want to remove selected major? (" + self.selected_major_Box.get(i) + ")"
            response = messagebox.askquestion("askquestion", msg, parent=t)
            if response == 'yes':
                self.selected_major_Box.delete(i)

        # insert selected minor into separate listbox
        def minorSelection(e):
            i = self.minorBox.curselection()
            self.selected_minor_Box.insert(END, self.minorBox.get(i))

        def removeMinor():
            i = self.selected_minor_Box.curselection()
            msg = "Do you want to remove selected minor? (" + self.selected_minor_Box.get(i) + ")"
            response = messagebox.askquestion("askquestion", msg, parent=t)
            if response == 'yes':
                self.selected_minor_Box.delete(i)

        def confirmSelection():
            self.setMajor_treeview()
            self.setMinor_treeview()
            self.editCareerButton.configure(state=NORMAL)
            t.destroy()

        mainframe = Frame(t)
        mainframe.pack(fill=X, ipadx=1, padx=10)

        majorframe = ttk.LabelFrame(mainframe, text="Major")
        majorframe.pack(side=LEFT, pady=5)

        minorframe = ttk.LabelFrame(mainframe, text="Minor")
        minorframe.pack(side=RIGHT, pady=5)

        self.schCbox1 = ttk.Combobox(majorframe, value=self.schList, exportselection=0, width=18)
        self.schCbox1.pack(side=TOP)
        self.schCbox1.bind("<<ComboboxSelected>>", self.getMajorBySchool)

        self.schCbox2 = ttk.Combobox(minorframe, value=self.schList, exportselection=0, width=18)
        self.schCbox2.pack(side=TOP)
        self.schCbox2.bind("<<ComboboxSelected>>", self.getMinorBySchool)

        self.majorVar = StringVar()
        self.majorBox = Listbox(majorframe, selectmode=SINGLE, justify=CENTER, listvariable=self.majorVar,
                                exportselection=False)
        # exportselection allows us to work on other listbox while not calling this binding
        self.majorBox.pack(side=TOP)
        self.majorBox.bind('<Double-1>', majorSelection)  # double-click binding

        self.minorVar = StringVar()
        self.minorBox = Listbox(minorframe, selectmode=SINGLE, justify=CENTER, listvariable=self.minorVar,
                                exportselection=False)
        self.minorBox.pack(side=TOP)
        self.minorBox.bind('<Double-1>', minorSelection)

        label3 = Label(majorframe, text="Major(s) Selected:")
        label3.pack(side=TOP)
        label4 = Label(minorframe, text="Minor(s) Selected:")
        label4.pack(side=TOP)

        self.selected_major_Box = Listbox(majorframe, selectmode=SINGLE, justify=CENTER, exportselection=False,
                                          height=5)
        self.selected_major_Box.pack(side=TOP)

        self.selected_minor_Box = Listbox(minorframe, selectmode=SINGLE, justify=CENTER, exportselection=False,
                                          height=5)
        self.selected_minor_Box.pack(side=TOP)

        # for if major & minor treeview were already filled
        for id in self.majorTree.get_children():
            major = self.majorTree.item(id)['text']
            self.selected_major_Box.insert(END, major)

        for id in self.minorTree.get_children():
            minor = self.minorTree.item(id)['text']
            self.selected_minor_Box.insert(END, minor)

        majorRemoveButton = ttk.Button(majorframe, text="Remove", command=removeMajor)
        majorRemoveButton.pack(side=TOP)
        minorRemoveButton = ttk.Button(minorframe, text="Remove", command=removeMinor)
        minorRemoveButton.pack(side=TOP)

        comfirmButton = ttk.Button(t, text="Confirm", command=confirmSelection)  # TODO: link to four year plan
        comfirmButton.pack(side=BOTTOM, pady=10)

    # end goal: return array of major under specified school
    def getMajorBySchool(self, e):
        pub.sendMessage("request_major", sch=self.schCbox1.get())

    def getMinorBySchool(self, e):
        pub.sendMessage("request_minor", sch=self.schCbox2.get())

    # fill major treeview from program planning worksheet
    def setMajor_treeview(self):
        for id in self.majorTree.get_children():  # clear tree view
            self.majorTree.delete(id)

        self.selected_major_Box.select_set(0, END)
        for i in self.selected_major_Box.curselection():
            word = self.selected_major_Box.get(i)
            self.majorTree.insert(parent='', index='end', iid=i, text=str(word))

    def setMinor_treeview(self):
        for id in self.minorTree.get_children():
            self.minorTree.delete(id)

        self.selected_minor_Box.select_set(0, END)
        for i in self.selected_minor_Box.curselection():
            word = self.selected_minor_Box.get(i)
            self.minorTree.insert(parent='', index='end', iid=i, text=str(word))

    def planningWorksheet_addCourseButton(self):
        t = Toplevel(self.mainwin)
        t.wm_title("Search for Course")
        t.geometry("450x125")
        t.resizable(width=FALSE, height=FALSE)
        t.transient(self.mainwin)
        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')

        def close(e):
            self.addCourseButton.configure(state=NORMAL)
            t.destroy()
        t.bind('<Destroy>', close)
        self.addCourseButton.configure(state=DISABLED)

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

        # adds searched course into the treeview
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

        courseEntryFrame = Frame(t)
        courseEntryFrame.pack(anchor=CENTER)

        l1 = Label(courseEntryFrame, text="Course Number:").pack(side=LEFT)
        entry = ttk.Entry(courseEntryFrame, width=10, justify=CENTER)
        entry.pack(side=LEFT)

        entry.bind('<KeyRelease>', courseSearch)  # for auto search

        resultFrame = Frame(t)
        resultFrame.pack(anchor=CENTER)

        resultEntry = ttk.Entry(resultFrame, textvariable=self.resultVar, state=DISABLED, justify=CENTER, width=50)
        resultEntry.pack(side=TOP)

        genedFrame = Frame(t)
        genedFrame.pack(anchor=CENTER)

        l2 = Label(genedFrame, text="gen ed/elect:").pack(side=LEFT, anchor=NW)

        genEntry = ttk.Entry(genedFrame)
        genEntry.pack(side=TOP)

        addButton = Button(genedFrame, text="Add", command=addCourse)
        addButton.pack(side=TOP)

    def planningWorksheet_delCourseButton(self):
        for course in self.courseTree.selection():
            msg = "Do you want to remove the selected course? (" + self.courseTree.item(course)['values'][0] + ")"
            response = messagebox.askquestion("askquestion", msg)
            if response == 'yes':
                prevcred = self.enrollCredVar.get()
                self.enrollCredVar.set(prevcred - int(float(self.courseTree.item(course)['values'][2])))

                self.courseTree.delete(course)
                self.courseTree_counter -= 1

    def planningWorksheet_addBackupCourseButton(self):
        t = Toplevel(self.mainwin)
        t.wm_title("Search for Backup Course")
        t.geometry("450x125")
        t.resizable(width=FALSE, height=FALSE)
        t.transient(self.mainwin)
        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')

        def close(e):
            self.addBackupButton.configure(state=NORMAL)
            t.destroy()
        t.bind('<Destroy>', close)
        self.addBackupButton.configure(state=DISABLED)

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

        courseEntryFrame = Frame(t)
        courseEntryFrame.pack(anchor=CENTER)

        l1 = Label(courseEntryFrame, text="Course Number:").pack(side=LEFT)
        entry = ttk.Entry(courseEntryFrame, width=10, justify=CENTER)
        entry.pack(side=LEFT)

        entry.bind('<KeyRelease>', courseSearch)  # for auto search

        resultFrame = Frame(t)
        resultFrame.pack(anchor=CENTER)

        resultEntry = ttk.Entry(resultFrame, textvariable=self.resultVar, state=DISABLED, justify=CENTER, width=50)
        resultEntry.pack(side=TOP)

        genedFrame = Frame(t)
        genedFrame.pack(anchor=CENTER)

        l2 = Label(genedFrame, text="gen ed/elect:").pack(side=LEFT, anchor=NW)

        genEntry = ttk.Entry(genedFrame)
        genEntry.pack(side=TOP)

        addButton = Button(genedFrame, text="Add", command=addCourse)
        addButton.pack(side=TOP)

    def planningWorksheet_delBackupCourseButton(self):
        for course in self.backupCourseTree.selection():
            msg = "Do you want to remove the selected backup course? (" + self.backupCourseTree.item(course)['values'][
                0] + ")"
            response = messagebox.askquestion("askquestion", msg)
            if response == 'yes':
                self.backupCourseTree.delete(course)
                self.backupCourseTree_counter -= 1

    # clears every widget
    def planningWorksheet_reset(self):
        self.courseHist.clear()
        self.nameEntry.delete(0, END)
        self.idEntry.delete(0, END)

        for id in self.majorTree.get_children():
            self.majorTree.delete(id)

        for id in self.minorTree.get_children():
            self.minorTree.delete(id)

        self.seasonVar.set("")

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

    def planningWorksheet_fill(self, obj, tcred, courses, numbCourse, major, minor, bcourses, courseHist, fourYear,
                               policies):
        # obj is a py dict

        # clear data in widgets
        self.planningWorksheet_reset()

        self.courseHist = courseHist
        self.nameEntry.insert(END, obj['name'])
        self.idEntry.insert(END, obj['s_id'])
        self.seasonVar.set(obj['registering_for'])

        index = 0
        for m in major:
            self.majorTree.insert(parent='', index='end', iid=index, text=m)
            index = index + 1
        index = 0
        for m in minor:
            self.minorTree.insert(parent='', index='end', iid=index, text=m)
            index = index + 1

        self.earnCredEntry['state'] = NORMAL
        self.earnCredEntry.insert(END, obj['credits'])
        self.earnCredEntry['state'] = 'readonly'

        self.enrollCredVar.set(tcred)

        self.enrlDateEntry.insert(END, obj['enrll'])
        self.memoEntry.insert('1.0', obj['memo'])

        for c in courses:
            self.courseTree.insert(parent='', index='end', iid=self.courseTree_counter, text="",
                                   values=(c[0], c[1], c[2], c[3]))
            self.courseTree_counter += 1

        for c in bcourses:
            self.backupCourseTree.insert(parent='', index='end', iid=self.backupCourseTree_counter, text="",
                                         values=(c[0], c[1], c[2], c[3]))
            self.backupCourseTree_counter += 1

        self.courseTakenList_fill()

    def fourYearPlan_fill(self, obj, tcred, courses, numbCourse, major, minor, bcourses, courseHist, fourYear,
                          policies):
        # delete what was previously there then insert
        self.name2Entry.delete(0, END)
        self.name2Entry.insert(END, obj['name'])

        self.id2Entry.delete(0, END)
        self.id2Entry.insert(END, obj['s_id'])

        self.policies = policies
        self.extraTable = []
        self.semTableTree_counter = 0
        semIndex = 0
        for sem in self.courseHist:
            for course in sem:
                self.progTable[semIndex].insert(parent='', index='end', iid=self.semTableTree_counter,
                                                values=(course[1] + " " + course[2], course[3], course[4]))
                self.semTableTree_counter += 1
            semIndex += 1

        majorIndex = 0
        for majors in fourYear:
            self.semTableTree_counter = 0
            semIndex = 0
            tabTitle = major[majorIndex]
            creation = False
            for sem in majors:
                for course in sem:
                    if majorIndex == 0:
                        self.tab_parent.tab(self.semesterFrame, text=tabTitle)

                        self.semTable[semIndex].insert(parent='', index='end', iid=self.semTableTree_counter,
                                                       values=(course[1] + " " + course[2], course[3], course[4]))

                        self.semTableTree_counter += 1

                        self.policyMemoEntry.delete('1.0', 'end')
                        self.policyMemoEntry.insert('1.0', policies[0])
                    else:
                        if creation == False:
                            yearCounter = 1
                            semesterCounter = 0
                            yPos = 50
                            extraLabel = []
                            yearCount = 0
                            self.newFrame = Frame(self.tab_parent, width=900, height=1375)
                            self.newFrame.pack(expand=1, fill='both')
                            self.tab_parent.add(self.newFrame, text=tabTitle)

                            """
                            for i in range(8):
                                if semesterCounter % 2 == 0:
                                    yearCount += 1
                                    self.extraTable.insert(i,
                                                           self.createTable("Year: " + str(yearCount), 15, yPos,
                                                                            self.extraTable,
                                                                            extraLabel,
                                                                            self.newFrame, semesterCounter))
                                else:
                                    self.extraTable.insert(i,
                                                           self.createTable(" ", 455, yPos, self.extraTable, extraLabel,
                                                                            self.newFrame, semesterCounter))
                                    yPos += 190
                                semesterCounter += 1
                            """
                            self.createTable(self.newFrame, extraLabel, self.extraTable)
                            creation = True
                        else:
                            self.extraTable[semIndex].insert(parent='', index='end', iid=self.semTableTree_counter,
                                                             values=(course[1] + " " + course[2], course[3], course[4]))
                            self.semTableTree_counter += 1
                semIndex += 1
            majorIndex += 1

    def FYP_reset(self):
        self.courseHist.clear()
        self.name2Entry.delete(0, END)
        self.id2Entry.delete(0, END)

        self.policyMemoEntry.delete('1.0', 'end')

        index = 0
        while (index < len(self.semTable)):
            for course in self.semTable[index].get_children():
                self.semTable[index].delete(course)
            index += 1
        index = 0
        while (index < len(self.progTable)):
            for course in self.progTable[index].get_children():
                self.progTable[index].delete(course)
            index += 1
        index = 0
        for object in self.extraTable:
            for course in object.get_children():
                self.extraTable[index].delete(course)
            index += 1

        self.tab_parent.tab(self.semesterFrame, text="Four Year Plan")
        while (self.tab_parent.index("end") != 2):
            self.tab_parent.forget(self.tab_parent.index("end") - 1)

    def FYP_addCourseButton(self):
        t = Toplevel(self.mainwin)
        t.wm_title("Search for Course")
        t.geometry("450x125")
        t.resizable(width=FALSE, height=FALSE)
        # t.attributes('-topmost', 'true')
        t.transient(self.mainwin)
        selectedTreeView = self.progressRepoFrame.focus_get()

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

        # adds searched course into the treeview
        def addCourse():
            print(selectedTreeView)
            selectedTreeView.insert(parent='', index='end', iid=self.progressRepo_counter, text="",
                                   values=(self.addCourseSearchResult[0] + self.addCourseSearchResult[1],
                                           self.addCourseSearchResult[2]))
            self.progressRepo_counter += 1

        courseEntryFrame = Frame(t)
        courseEntryFrame.pack(anchor=CENTER)

        l1 = Label(courseEntryFrame, text="Course Number:").pack(side=LEFT)
        entry = ttk.Entry(courseEntryFrame, width=10, justify=CENTER)
        entry.pack(side=RIGHT)

        entry.bind('<KeyRelease>', courseSearch)  # for auto search

        resultFrame = Frame(t)
        resultFrame.pack(anchor=CENTER)

        resultEntry = ttk.Entry(resultFrame, textvariable=self.resultVar, state=DISABLED, justify=CENTER, width=50)
        resultEntry.pack(pady=10)

        addButton = Button(resultFrame, text="Add", command=addCourse)
        addButton.pack(side=BOTTOM, pady=5)

    def FYP_delCourseButton(self):
        selectedTreeView = self.progressRepoFrame.focus_get()
        for course in selectedTreeView.selection():
            msg = "Do you want to remove the selected course? (" + selectedTreeView.item(course)['values'][0] + ")"
            response = messagebox.askquestion("askquestion", msg)
            if response == 'yes':
                selectedTreeView.delete(course)
                self.progressRepo_counter -= 1

    def updatePolicy(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        tab_index = event.widget.index(selected_tab)
        if tab_text == "Progress Report" or tab_text == "Four Year Plan":
            print()
        else:
            self.policyMemoEntry.delete('1.0', 'end')
            self.policyMemoEntry.insert('1.0', self.policies[tab_index - 1])

    def courseTakenList_layout(self):
        label = Label(self.courseTakenListFrame, text="Course Taken List", font=('Helvetica', 19))
        label.pack(anchor=CENTER, side=TOP, pady=20)

        self.courseTakenListTree = ttk.Treeview(self.courseTakenListFrame, show="tree", height=38,
                                                style="mystyle.Treeview")
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
                        name = str(course[1] + " " + course[2] + " " * 5 + course[3])
                        self.courseTakenListTree.insert(parent=str(id), index='end', iid=self.courseTakenList_counter,
                                                        text=name, values=(course[5]))
                        self.courseTakenList_counter += 1

        for id in self.courseTakenListTree.get_children():
            if not self.courseTakenListTree.get_children(id):
                self.courseTakenListTree.delete(id)

    def menuBar(self):
        menu = Menu(self.mainwin, tearoff=0)
        self.mainwin.config(menu=menu)

        self.schedule = Menu(menu, tearoff=0)
        menu.add_cascade(label='Schedule', menu=self.schedule)
        self.scheduleMenu()

        load = Menu(menu, tearoff=0)
        menu.add_cascade(label='View', menu=load)
        self.loadMenu(load)

        # DataBase
        DB = Menu(menu, tearoff=0)
        menu.add_cascade(label='Update DB', menu=DB)
        self.DataBaseMenu(DB)

    # schedule menu dropdown
    def scheduleMenu(self):
        self.schedule.add_command(label='New', command=self.newSchedule)
        self.schedule.add_command(label='Open...', command=self.openSchedule)
        self.schedule.add_separator()
        self.schedule.add_command(label='Save', command=self.saveSchedule)
        self.schedule.add_separator()
        self.schedule.add_command(label='Export', command=self.exportSchedule)
        self.schedule.add_command(label='Print', command=self.printSchedule)

    def newSchedule(self):
        self.planningWorksheet_reset()
        self.FYP_reset()
        self.courseTakenList_reset()

    def openSchedule(self):
        t = Toplevel(self.mainwin)
        t.wm_title("Search for Student")
        t.geometry("450x125")
        t.resizable(width=0, height=0)
        t.attributes('-topmost', 'true')
        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')

        def close(e):
            self.schedule.entryconfigure(1, state=NORMAL)
            t.destroy()
        t.bind('<Destroy>', close)
        self.schedule.entryconfigure(1, state=DISABLED)

        def openScheduleSearchButton():
            name = fnameE.get() + " " + lnameE.get()
            id = idE.get()
            if name != "" and id != "":
                pub.sendMessage("request_PPW", name=name, id=int(id))
                self.schedule.entryconfigure(1, state=NORMAL)
                t.destroy()

        nameFrame = Frame(t)
        nameFrame.pack(side=TOP, anchor='w', padx=20, pady=10)

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
        majors, minors = [], []
        for id in self.majorTree.get_children():
            majors.append(self.majorTree.item(id)['text'])
        for id in self.minorTree.get_children():
            minors.append(self.minorTree.item(id)['text'])

        courses, bcourses = [], []
        for id in self.courseTree.get_children():
            courses.append(self.courseTree.item(id)['values'])
        for id in self.backupCourseTree.get_children():
            bcourses.append(self.backupCourseTree.item(id)['values'])

        pydict = {
            "name": self.nameEntry.get(),
            "s_id": self.idEntry.get(),
            # "dept": ,
            "major": majors,
            "minor": minors,
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
        self.courseTakenListFrame.pack_forget()
        self.leftFrame.pack(side=LEFT, fill=Y)

    def showCourseTakenList(self):
        self.leftFrame.pack_forget()
        self.courseTakenListFrame.pack(side=LEFT, fill=Y)
        self.courseTakenListFrame['width'] = self.left_width
        self.courseTakenListFrame.propagate(0)

    # data base menu dropdown
    def DataBaseMenu(self, DB):
        DB.add_command(label='Current Semester Course')
        DB.add_separator()
        DB.add_command(label='Add/Remove a School')
        DB.add_command(label='Add/remove a Major')
        DB.add_command(label='Add/Remove a minor')

    """"
    def createTable(self, semester, x, y, tableArray, labelArray, frame, counter):
        endOfArray = len(tableArray)
        endOfSemLabel = len(labelArray)

        labelArray.append(Label(frame, text=semester, font=('Helvetica', 15)))
        labelArray[endOfSemLabel].pack(expand=1)

        tableArray.append(ttk.Treeview(frame, height=7, style="mystyle.Treeview"))

        if counter % 2 == 0:
            tableArray[endOfArray].pack(expand=1)
            tableArray[endOfArray].place(x=15, y=y)
            labelArray[endOfSemLabel].place(x=15, y=y - 25)
        else:
            tableArray[endOfArray].pack(expand=1)
            tableArray[endOfArray].place(x=455, y=y)
            labelArray[endOfSemLabel].place(x=455, y=y - 25)

        tableArray[endOfArray]['columns'] = ("course#", "title", "cred")
        tableArray[endOfArray].column("#0", width=0, stretch=NO)  # important
        tableArray[endOfArray].column("course#", anchor=CENTER, width=75)  # anchor for the data in the column
        tableArray[endOfArray].column("title", anchor=W, width=295)
        tableArray[endOfArray].column("cred", anchor=CENTER, width=25)
        # self.semesterTree.column("taken", anchor=CENTER, width=30)

        tableArray[endOfArray].heading("course#", text='Course #', anchor=CENTER)  # anchor for the title of the column
        tableArray[endOfArray].heading("title", text='Title', anchor=CENTER)
        tableArray[endOfArray].heading("cred", text='CR', anchor=CENTER)

        return tableArray[endOfArray]

    def createSemesterBtn(self, semester, y, tableArray, labelArray, frame, counter):
        if counter % 2 == 0:
            self.createTable(semester, 15, self.tempY, tableArray, labelArray, frame, self.temp)
            self.addSemesterBtn.place(x=455, y=self.tempY)
        else:
            self.createTable(semester, 455, self.tempY, tableArray, labelArray, frame, self.temp)
            self.tempY += 190
            self.addSemesterBtn.place(x=15, y=self.tempY)
        self.temp += 1
    """
