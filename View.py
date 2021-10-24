import tkinter
from tkinter import *
from tkinter import ttk

# import tkinter as tk
# from ttkthemes import ThemedTk
from tkinter.messagebox import showinfo

from pubsub import pub  # pip install PyPubSub
import tkinter.font as TkFont
import math
import requests
import json
# from PIL import ImageTk, Image  # pip install pillow
from tkinter import messagebox


class View:
    def __init__(self, master):
        self.mainwin = master
        self.mainwin.title("Academic Advising Tool")
        self.mainwin.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))
        # self.mainwin.protocol("WM_DELETE_WINDOW", self.on_closing)

        # self.mainwin.resizable(width=0, height=0)
        # 2560 x 1440
        self.mainwin.deiconify()

        # self.mainwin.call('tk', 'scaling', 0.75)

        self.defaultFont = TkFont.nametofont("TkDefaultFont")
        self.defaultFont.configure(family='Helvetica', size=10)

        self.TVstyle = ttk.Style()
        self.TVstyle.configure("mystyle.Treeview", font=('Helvetica', 10))
        self.TVstyle.configure("mystyle.Treeview.Heading", font=('Helvetica', 10))

        self.schList = []
        self.subjectsList = []

        self.courseTree_counter = 0
        self.backupCourseTree_counter = 0
        self.courseTakenList_counter = 0
        self.addCourseSearchResult = []
        self.resultVar = StringVar()  # for add course button
        self.sizeOfMinor = 0
        self.studentsVar = []
        self.studentIdsVar = []

        self.courseHist = []

        self.winSumTable = []
        self.winSumLabel = []

        self.backup_course_regex_list = {}
        self.course_regex_list = {}
        self.policy_to_display = []
        # self.memo_to_display = ""

        self.majorsTable = []  # Holds arrays filled with treeviews
        self.minorsTable = []  # Holds arrays filled with treeviews
        self.majorFrames = []  # Holds frames major for tabs
        self.minorFrames = []  # Holds frames minor for tabs
        self.majorsLabelArray = []  # Holds labels for major tabs
        self.minorsLabelArray = []  # Holds labels for minor tabs
        self.majors = []
        self.minors = []
        self.majorsFYP = []
        self.selectedSemester = 0

        self.loginPage()
        self.menuBar()
        self.loginWindow.protocol("WM_DELETE_WINDOW",
                                  self.login_closing)  # If user closes login window application closes

    # prompt message before closing program,
    # also closes all TopLevel functions

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            for widget in self.mainwin.winfo_children():
                if isinstance(widget, Toplevel):
                    widget.destroy()
            self.mainwin.destroy()

    def login_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?", parent=self.loginWindow):
            for widget in self.mainwin.winfo_children():
                if isinstance(widget, Toplevel):
                    widget.destroy()
            self.loginWindow.destroy()
            self.mainwin.destroy()

    def layout(self):

        self.right_width = self.mainwin.winfo_screenwidth() * 0.4
        self.left_width = self.mainwin.winfo_screenwidth() - self.right_width

        self.mainFrame = ttk.Frame(self.mainwin)
        self.mainFrame.pack(fill=BOTH, padx=10, pady=10, expand=1, ipadx=10)

        # four year plan
        self.leftFrame = ttk.Frame(self.mainFrame, width=self.left_width, borderwidth=2, relief=GROOVE)
        self.leftFrame.pack(side=LEFT, fill=Y, padx=5)

        # program planning worksheet
        self.PPWFrame = ttk.Frame(self.mainFrame, width=self.right_width, borderwidth=2, relief=GROOVE)
        self.PPWFrame.pack(side=RIGHT, fill=Y)
        self.PPWFrame.pack_propagate(0)

        self.courseTakenListFrame = ttk.Frame(self.mainFrame, width=self.left_width, borderwidth=2, relief=GROOVE)
        self.courseTakenListFrame.pack(side=LEFT, fill=Y, padx=5)
        # self.courseTakenListFrame.pack_propagate(0)
        self.courseTakenListFrame.pack_forget()  # hide frame

        self.FourYearPlan()
        self.planningWorksheet_layout()
        self.courseTakenList_layout()

    def loginPage(self):
        verify = 0
        self.loginWindow = Toplevel(self.mainwin)
        self.loginWindow.wm_title("Login")
        self.loginWindow.geometry("300x155")
        self.loginWindow.resizable(width=0, height=0)
        self.loginWindow.attributes('-topmost', 'true')
        self.mainwin.eval(f'tk::PlaceWindow {str(self.loginWindow)} center')
        self.loginWindow.grab_set()

        loginFrame = Frame(self.loginWindow)
        emailFrame = Frame(self.loginWindow, width=30)
        passwrdFrame = Frame(self.loginWindow, width=30)

        loginBtn = Button(loginFrame, text="Login", font=('Helvetica', 10))

        emailLabel = Label(emailFrame, text="Email: ", font=('Helvetica', 10), padx=55)
        passwrdLabel = Label(passwrdFrame, text="Password: ", font=('Helvetica', 10), padx=55)
        wrongPassLabel = Label(loginFrame, text="No matching credentials, please try again", font=('Helvetica', 10))

        self.emailEntry = Entry(emailFrame, width=30)
        self.passwrdEntry = Entry(passwrdFrame, width=30)

        emailFrame.pack(side=TOP, fill=X, pady=5)
        passwrdFrame.pack(side=TOP, fill=X, pady=5)
        loginFrame.pack(fill='both')

        wrongPassLabel.pack(side=BOTTOM)
        wrongPassLabel.forget()
        loginBtn.pack(side=BOTTOM)
        emailLabel.pack(side=TOP, anchor=W)
        passwrdLabel.pack(side=TOP, anchor=W)
        self.emailEntry.pack(side=BOTTOM)
        self.passwrdEntry.pack(side=BOTTOM)

        def checkLogin(e):
            url = "https://cosc426restapi.herokuapp.com/api/user/login/"
            restAPIEmail = 'testing@email.com'
            restAPIpasswrd = 'test123'
            user = self.emailEntry.get()
            pwd = self.passwrdEntry.get()
            val = {
                "email": restAPIEmail,
                "password": restAPIpasswrd
            }
            response = requests.post(url, json=val)
            obj = response

            if obj.text.startswith('v2.public'):
                val = obj.text
                self.loginWindow.grab_release()
                self.loginWindow.destroy()
                self.mainwin.lift()
                pub.sendMessage("request_setAuthToken", tok=val)
                pub.sendMessage("request_allSchools")
                pub.sendMessage("request_allSubjects")
                self.layout()

            else:
                wrongPassLabel = Label(emailFrame, text=obj.text, font=('Helvetica', 10), padx=55)
                loginBtn.forget()
                wrongPassLabel.pack(side=BOTTOM)
                loginBtn.pack(side=BOTTOM)

        loginBtn.bind("<Button-1>", checkLogin)

    def FourYearPlan(self):
        # ============================ Scroll Bar ============================
        self.canvas = Canvas(self.leftFrame, width=self.left_width)  # Creating Canvas for scrollbar
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.scrollbar = ttk.Scrollbar(self.leftFrame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.innerLeftFrame = Frame(self.canvas)
        self.innerLeftFrame.pack(expand=1)

        self.canvas.create_window((0, 0), window=self.innerLeftFrame, anchor=NW, width=self.left_width)

        # ============================ title ============================
        FYPTitleFrame = Frame(self.innerLeftFrame, width=self.left_width, height=50)
        FYPTitleFrame.pack(pady=20)

        FYPTitle = ttk.Label(FYPTitleFrame, text="Academic Advising", anchor=CENTER,
                             font=('Helvetica', 19))
        FYPTitle.pack(side=TOP)

        # ============================ Student Name and ID ============================

        nameIDFrame = Frame(self.innerLeftFrame, width=self.left_width, height=50)
        nameIDFrame.pack(ipadx=30, ipady=10)

        nameLabel = Label(nameIDFrame, text='Name:')
        nameLabel.pack(side=LEFT, expand=1)

        self.FYPnameEntry = ttk.Entry(nameIDFrame)
        self.FYPnameEntry.pack(side=LEFT, expand=1)

        self.id2Entry = ttk.Entry(nameIDFrame, width=8)
        self.id2Entry.pack(side=RIGHT, expand=1)

        idLabel = Label(nameIDFrame, text='ID Number:')
        idLabel.pack(side=RIGHT, expand=1)

        # ============================ Progress Report ============================
        # Creation of ttk.Notebook to add tabs to Academic Advising screen
        self.tab_parent = ttk.Notebook(self.innerLeftFrame)

        # Frame for Progress Report tab
        self.progressRepoFrame = Frame(self.tab_parent, width=self.left_width)
        self.progressRepoFrame.pack(fill='both')

        # Event handler to change policy via clicking a tab
        self.tab_parent.bind('<ButtonRelease>', self.updatePolicy)
        self.tab_parent.pack(expand=1, fill=X, pady=30, ipady=5)

        self.progLabel = []  # Holds the labels for each semester in Progress Report
        self.progTable = []  # Holds the treeviews for progress report

        # Treeviews are created for Progress Report tab
        self.createTable(self.progressRepoFrame, self.progLabel, self.progTable, 8)

        # Adds the progress report tab ttk.Notebook
        self.tab_parent.add(self.progressRepoFrame, text="Progress Report")

        # Creating buttons for Progress Report placing with .grid() in FYP_addCourseButton
        self.addProgRepoBtn = Button(self.progressRepoFrame, text="Add", command=lambda: self.FYP_addCourseButton())
        self.removeProgRepoBtn = Button(self.progressRepoFrame, text="Remove", command=lambda: self.FYP_delCourseButton(self.mainwin))

        # ============================ Add Semester Table Button ============================
        """
        self.addSemesterBtn = Button(self.semesterFrame, text="Add a semester")
        self.addSemesterBtn.pack()
        self.addSemesterBtn.place(x=120, y=950)
        self.temp = semesterCounter
        self.tempY = yPos
        self.addSemesterBtn['command'] = lambda: self.createSemesterBtn("Extra Semester", self.tempY, self.semTable,
                                                                        self.semLabel, self.semesterFrame, self.temp)
        """



    def fourYearPlan_fill(self, obj, tcred, courses, numbCourse, major, minor, bcourses,
                          courseHist, fourYear, minorFourYear, minorReqList, policies,
                          sumCourse, winCourse):
        # delete what was previously there then insert

        self.FYP_reset()

        self.FYPnameEntry.delete(0, END)
        self.FYPnameEntry.insert(END, obj['name'])

        self.id2Entry.delete(0, END)
        self.id2Entry.insert(END, obj['s_id'])

        self.FYPnameEntry.config(state=DISABLED)
        self.id2Entry.config(state=DISABLED)

        self.minorReqList = minorReqList  # Copying minor requirements to use as labels for creatTable()
        self.policies = policies  # Copying policies for other functions
        self.courseHist = courseHist
        if len(courseHist) % 2 == 0:
            self.progTableLength = len(
                courseHist) + 2  # Storing the amount of semesters to make that many treeviews in createTable
        else:
            self.progTableLength = len(
                courseHist) + 1  # Storing the amount of semesters to make that many treeviews in createTable
        self.majorsTable = []  # Holds arrays filled with treeviews
        self.minorsTable = []  # Holds arrays filled with treeviews
        self.majorFrames = []  # Holds frames major for tabs
        self.minorFrames = []  # Holds frames minor for tabs
        self.majorsLabelArray = []  # Holds labels for major tabs
        self.minorsLabelArray = []  # Holds labels for minor tabs

        self.progTableTree_iid = 0  # Tracks iid for Progress Report treeviews
        self.majorsTableTree_iid = 0  # Tracks iid for major tables treeviews

        # Destroying and re-creating progress report to handle dynamic amount of semesters
        for i in self.progTable:
            i.destroy()
        for i in self.progLabel:
            i.destroy()

        self.progTable.clear()
        self.progLabel.clear()

        # CLearing any tabs that might exist before displaying student
        while (self.tab_parent.index("end") != 1):  # Removes the tabs but leaves Progress Report tab
            self.tab_parent.forget(self.tab_parent.index("end") - 1)

        # Treeviews are re-created for Progress Report tab with number of semesters student has taken
        self.createTable(self.progressRepoFrame, self.progLabel, self.progTable, self.progTableLength)

        # Filling winter and summer courses
        self.winSumTable = []
        self.winSumLabel = []

        self.createWinSumTable(self.progressRepoFrame, self.winSumLabel, self.winSumTable, self.progTableLength + 1)

        # Updates canvas to get correct scrollbar size
        self.canvas.update()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        semIndex = 0
        for sem in courseHist:  # Filling the Progress Report treeviews with students course history from database
            self.progTableTree_iid = 0
            for course in sem:
                self.progTable[semIndex].insert(parent='', index='end', iid=self.progTableTree_iid,
                                                values=(course[1] + " " + course[2], course[3], course[4]))
                self.progTableTree_iid += 1
            semIndex += 1

        # Filling the Progress Report winter summer treeviews
        iid = 0
        for course in winCourse:
            self.winSumTable[0].insert(parent='', index='end', iid=iid,
                                       values=(course[0] + " " + course[1], course[2], course[3]))
            iid += 1

        iid = 0
        for course in sumCourse:
            self.winSumTable[1].insert(parent='', index='end', iid=iid,
                                       values=(course[0] + " " + course[1], course[2], course[3]))
            iid += 1

        for i in range(len(major)):  # Filling arrays according to amount of majors a student is doing
            self.majorsLabelArray.append([])  # Creates 2d array for each each array containing labels for a tab
            self.majorsTable.append([])  # Creates 2d array each array is a major containing each treeview for a tab
            self.majorFrames.append(Frame(self.tab_parent))  # Holds frames for each tab
            self.createTable(self.majorFrames[i], self.majorsLabelArray[i], self.majorsTable[i],
                             8)  # Function to populate these arrays
            self.tab_parent.add(self.majorFrames[i], text=major[i])  # Each frame to the ttk.Notebook to display tab
            policy_button = Button(self.majorFrames[i], text="University Policy",
                                   command=lambda: self.univ_policy_box())
            policy_button.grid(column=0, row=0, columnspan=1, sticky=E, padx=150)

        for i in range(len(minor)):  # Filling arrays according to amount of majors a student is doing
            self.sizeOfMinor = len(self.minorReqList[i])  # Amount of tables and labels for each minor
            self.minorsLabelArray.append([])  # Creates 2d array for each each array containing labels for a tab
            self.minorsTable.append([])  # Creates 2d array each array is a minor containing each treeview for a tab
            self.minorFrames.append(Frame(self.tab_parent))  # Holds frames for each tab
            self.createMinorTable(self.minorFrames[i], self.minorsLabelArray[i],
                                  self.minorsTable[i])  # Function to populate these arrays
            self.tab_parent.add(self.minorFrames[i], text=minor[i])  # Each frame to the ttk.Notebook to display tab
            policy_button = Button(self.minorFrames[i], text="University Policy",
                                   command=lambda: self.univ_policy_box())
            policy_button.grid(column=0, row=0, columnspan=1, sticky=E, padx=150)

        majorIndex = 0
        for majors in fourYear:  # Filling semesters for each major tab
            semIndex = 0
            for sem in majors:
                self.majorsTableTree_iid = 0
                for course in sem:
                    self.majorsTable[majorIndex][semIndex].insert(parent='', index='end',
                                                                  iid=self.majorsTableTree_iid,
                                                                  values=(str(course[1] + " " + course[2]), course[3],
                                                                          course[4]))
                    self.majorsTableTree_iid += 1
                semIndex += 1
            majorIndex += 1

        minorIndex = 0
        for minors in minorFourYear:  # Filling semesters for each minor tab
            semIndex = 0
            for sem in minors:
                self.minorTableTree_iid = 0
                for course in sem:
                    self.minorsTable[minorIndex][semIndex].insert(parent='', index='end',
                                                                  iid=self.minorTableTree_iid,
                                                                  values=(str(course[1] + " " + course[2]), course[3],
                                                                          course[4]))
                    self.minorTableTree_iid += 1
                semIndex += 1
            minorIndex += 1

        for minors in range(len(self.minorReqList)):
            for labels in range(len(self.minorReqList[minors])):
                self.minorsLabelArray[minors][labels]['text'] = self.minorReqList[minors][labels][1]

    def fourYearPlan_refresh(self, major, minor, FourYear, minorFourYear, minorReqList, policies):
        self.minorReqList = minorReqList  # Copying minor requirements to use as labels for creatTable()
        self.policies = policies  # Copying policies for other functions
        self.majorsTable = []  # Holds arrays filled with treeviews
        self.minorsTable = []  # Holds arrays filled with treeviews
        self.majorFrames = []  # Holds frames major for tabs
        self.minorFrames = []  # Holds frames minor for tabs
        self.majorsLabelArray = []  # Holds labels for major tabs
        self.minorsLabelArray = []  # Holds labels for minor tabs
        self.minorLength = len(minor)
        self.progTableTree_iid = 0  # Tracks iid for Progress Report treeviews
        self.majorsTableTree_iid = 0  # Tracks iid for major tables treeviews

        for i in range(len(major)):  # Filling arrays according to amount of majors a student is doing
            self.majorsLabelArray.append([])  # Creates 2d array for each each array containing labels for a tab
            self.majorsTable.append([])  # Creates 2d array each array is a major containing each treeview for a tab
            self.majorFrames.append(Frame(self.tab_parent))  # Holds frames for each tab
            self.createTable(self.majorFrames[i], self.majorsLabelArray[i], self.majorsTable[i],
                             8)  # Function to populate these arrays
            self.tab_parent.add(self.majorFrames[i], text=major[i])  # Each frame to the ttk.Notebook to display tab

        for i in range(len(minor)):  # Filling arrays according to amount of majors a student is doing
            self.sizeOfMinor = len(self.minorReqList[i])  # Amount of tables and labels for each minor
            self.minorsLabelArray.append([])  # Creates 2d array for each each array containing labels for a tab
            self.minorsTable.append([])  # Creates 2d array each array is a minor containing each treeview for a tab
            self.minorFrames.append(Frame(self.tab_parent))  # Holds frames for each tab
            self.createMinorTable(self.minorFrames[i], self.minorsLabelArray[i],
                                  self.minorsTable[i])  # Function to populate these arrays
            self.tab_parent.add(self.minorFrames[i], text=minor[i])  # Each frame to the ttk.Notebook to display tab

        majorIndex = 0
        for majors in FourYear:  # Filling semesters for each major
            semIndex = 0
            for sem in majors:
                self.majorsTableTree_iid = 0
                for course in sem:
                    self.majorsTable[majorIndex][semIndex].insert(parent='', index='end',
                                                                  iid=self.majorsTableTree_iid,
                                                                  values=(str(course[1] + " " + course[2]), course[3],
                                                                          course[4]))
                    self.majorsTableTree_iid += 1
                semIndex += 1
            majorIndex += 1

        minorIndex = 0
        for minors in minorFourYear:  # Filling semesters for each minor
            semIndex = 0
            for sem in minors:
                self.minorTableTree_iid = 0
                for course in sem:
                    self.minorsTable[minorIndex][semIndex].insert(parent='', index='end',
                                                                  iid=self.minorTableTree_iid,
                                                                  values=(str(course[1] + " " + course[2]), course[3],
                                                                          course[4]))
                    self.minorTableTree_iid += 1
                semIndex += 1
            minorIndex += 1

        for minors in range(len(self.minorReqList)):
            for labels in range(len(self.minorReqList[minors])):
                self.minorsLabelArray[minors][labels]['text'] = self.minorReqList[minors][labels][1]

    def FYP_reset(self):
        self.FYPnameEntry.delete(0, END)
        self.id2Entry.delete(0, END)
        self.FYPnameEntry.config(state=NORMAL)
        self.id2Entry.config(state=NORMAL)
        for sem in self.progTable:  # Clear courses in treeviews under Progress Report tab
            for course in sem.get_children():
                sem.delete(course)

        if self.winSumTable:
            for sem in self.winSumTable:  # Clear winter/summer courses in treeviews under Progress Report tab
                for course in sem.get_children():
                    sem.delete(course)

        if self.winSumTable:
            for sem in self.winSumTable:  # Clear treeviews in Progress Report tab
                sem.destroy()

        for sem in self.winSumLabel:  # Clear treeviews in Progress Report tab
            sem.destroy()

        for i in self.progTable:
            i.destroy()
        for i in self.progLabel:
            i.destroy()

        self.progTable.clear()
        self.progLabel.clear()

        self.createTable(self.progressRepoFrame, self.progLabel, self.progTable, 8)

        # Updates canvas to get correct scrollbar size
        self.canvas.update()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        if self.majorsTable:
            for majors in self.majorsTable:  # Clear treeviews for each major tab
                for sem in majors:
                    for course in sem.get_children():
                        sem.delete(course)
        if self.minorsTable:
            for minors in self.minorsTable:  # Clear treeviews for each minor tab
                for sem in minors:
                    for course in sem.get_children():
                        sem.delete(course)

        self.majorsTable.clear()
        self.minorsTable.clear()
        self.majorsLabelArray.clear()
        self.minorsLabelArray.clear()
        self.majorFrames.clear()
        self.minorFrames.clear()
        self.winSumTable.clear()
        self.winSumLabel.clear()

        while (self.tab_parent.index("end") != 1):  # Removes the tabs but leaves Progress Report tab
            self.tab_parent.forget(self.tab_parent.index("end") - 1)

    def FYP_addCourseButton2(self, parentWindow):
        t = Toplevel(parentWindow)
        t.wm_title("Search for Course")
        t.geometry("450x125")
        t.resizable(width=FALSE, height=FALSE)
        # t.attributes('-topmost', 'true')
        t.transient(self.mainwin)

        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')
        t.attributes('-topmost', 'true')
        selectedTreeView = self.mainwin.focus_get()
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
            selectedTreeView.insert(parent='', index='end', iid=(len(selectedTreeView.get_children()) + 1), text="",
                                    values=(self.addCourseSearchResult[0] + self.addCourseSearchResult[1],
                                            self.addCourseSearchResult[2]))

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

    def FYP_delCourseButton(self, parentWindow):
        selectedTreeView = self.mainwin.focus_get()

        for course in selectedTreeView.selection():
            msg = "Do you want to remove the selected course? (" + selectedTreeView.item(course)['values'][0] + ")"
            response = messagebox.askquestion("askquestion", msg)
            parentWindow.lower()
            if response == 'yes':
                selectedTreeView.delete(course)

    # Function for event handler to change policy memo via clicking a tab
    def updatePolicy(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        tab_index = event.widget.index(selected_tab)
        if tab_text == "Progress Report":
            pass
        else:
            pub.sendMessage('request_Policy_to_Display', policy=self.policies[tab_index - 1])

        self.canvas.update()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Creates a table of treeviews for progress report tab
    def createTable(self, frame, labels, tables, length):

        # column configure
        for i in range(2):
            frame.columnconfigure(i, weight=1)

        # define treeviews and labels
        for i in range(length):
            tables.append(
                ttk.Treeview(frame, height=7, style="mystyle.Treeview", takefocus=True, selectmode="none"))

            tables[i]['columns'] = ("course#", "title", "cred")
            tables[i].column("#0", width=0, stretch=NO)
            tables[i].column("course#", anchor=CENTER, width=90)
            w = int((self.left_width - 300) / 2)
            tables[i].column("title", anchor=W, width=w)
            tables[i].column("cred", anchor=CENTER, width=35)
            # tables[i].column("taken", anchor=CENTER, width=30)

            tables[i].heading("course#", text='Course #', anchor=CENTER)
            tables[i].heading("title", text='Title', anchor=CENTER)
            tables[i].heading("cred", text='CR', anchor=CENTER)

            if i < math.floor(length / 2):
                labels.append(Label(frame, text="Year " + str(i + 1), font=('Helvetica', 15)))

        # grid labels
        for i in range(math.floor(length / 2)):
            labels[i].grid(column=0, row=2 * i, columnspan=2, sticky=W, padx=5)

        # grid treeviews
        for i in range(0, length - 1, 2):
            tables[i].grid(column=0, row=i + 1)
            tables[i + 1].grid(column=1, row=i + 1)

    # Creates a table of treeviews for minor tabs
    def createMinorTable(self, frame, labels, tables):
        # column configure
        for i in range(2):
            frame.columnconfigure(i, weight=1)
        # define treeviews and labels
        for i in range(self.sizeOfMinor):  # Looping through the amount of minors
            tables.append(ttk.Treeview(frame, height=7, style="mystyle.Treeview", takefocus=True))

            tables[i]['columns'] = ("course#", "title", "cred")
            tables[i].column("#0", width=0, stretch=NO)
            tables[i].column("course#", anchor=CENTER, width=90)
            w = int((self.left_width - 300) / 2)
            tables[i].column("title", anchor=W, width=w)
            tables[i].column("cred", anchor=CENTER, width=35)
            # tables[i].column("taken", anchor=CENTER, width=30)

            tables[i].heading("course#", text='Course #', anchor=CENTER)
            tables[i].heading("title", text='Title', anchor=CENTER)
            tables[i].heading("cred", text='CR', anchor=CENTER)

            if i < len(tables):
                labels.append(Label(frame, font=('Helvetica', 12)))

            # grid labels
            row = 0
            for i in range(len(tables)):
                if i % 2 == 0:
                    tables[i].grid(column=0, row=row + 2)
                    labels[i].grid(column=0, row=row + 1, columnspan=1, sticky=W, padx=5)
                else:
                    tables[i].grid(column=1, row=row + 2)
                    labels[i].grid(column=1, row=row + 1, columnspan=1, sticky=W, padx=5)
                    row += 2

    # Creates a table of treeviews for tabs in Academic Advising
    def createWinSumTable(self, frame, labels, tables, length):
        # column configure
        for i in range(2):
            frame.columnconfigure(i, weight=1)

        # define treeviews and labels
        for i in range(2):
            tables.append(ttk.Treeview(frame, height=7, style="mystyle.Treeview", takefocus=True))

            tables[i]['columns'] = ("course#", "title", "cred")
            tables[i].column("#0", width=0, stretch=NO)
            tables[i].column("course#", anchor=CENTER, width=90)
            w = int((self.left_width - 300) / 2)
            tables[i].column("title", anchor=W, width=w)
            tables[i].column("cred", anchor=CENTER, width=35)
            # tables[i].column("taken", anchor=CENTER, width=30)

            tables[i].heading("course#", text='Course #', anchor=CENTER)
            tables[i].heading("title", text='Title', anchor=CENTER)
            tables[i].heading("cred", text='CR', anchor=CENTER)

        labels.append(Label(frame, text="Winter Courses", font=('Helvetica', 15)))
        labels.append(Label(frame, text="Summer Courses", font=('Helvetica', 15)))

        labels[0].grid(column=0, row=length + 1, columnspan=2, sticky=W, padx=5)
        tables[0].grid(column=0, row=length + 2)

        labels[1].grid(column=1, row=length + 1, columnspan=2, sticky=W, padx=5)
        tables[1].grid(column=1, row=length + 2)

    def FYP_addCourseButton(self):
        t = Toplevel(self.mainwin)
        t.wm_title("Search for Course")
        t.geometry("700x500")
        t.resizable(width=FALSE, height=FALSE)
        t.transient(self.mainwin)
        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')

        def close(e):
            self.addCourseButton.configure(state=NORMAL)
            t.destroy()

        t.bind('<Destroy>', close)
        self.addCourseButton.configure(state=DISABLED)

        def update_course_list(data):
            for i in self.course_tree.get_children():
                self.course_tree.delete(i)

            #self.course_tree.tag_configure('evenrow', background="grey")
            #self.course_tree.tag_configure('oddrow', background="white")

            for item in data:
                self.course_tree.insert('', 'end',
                                   values=(item['Subject'], item['Catalog'], item['Long Title'], item['Allowd Unt']))

        def fillout_fields(event):
            subject_entry.delete(0, END)
            catalog_entry.delete(0, END)
            title_entry.delete(0, END)
            credit_entry.delete(0, END)

            course = self.course_tree.focus()
            course_info = self.course_tree.item(course)['values']

            subject_entry.insert(0, course_info[0])
            catalog_entry.insert(0, course_info[1])
            title_entry.insert(0, course_info[2])
            credit_entry.insert(0, course_info[3])

        def check_course(event):
            subject_type = subject_entry.get().upper()
            catalog_type = catalog_entry.get()
            title_type = title_entry.get().upper()
            credit_type = credit_entry.get()

            pub.sendMessage("request_Course_by_Regex", sub=subject_type, cat=catalog_type, title=title_type, cred=credit_type)
            update_course_list(self.course_regex_list)

        # adds searched course into the treeview
        def addCourse():
            subject_type = subject_entry.get().upper()
            catalog_type = catalog_entry.get()
            title_type = title_entry.get().upper()
            credit_type = credit_entry.get()
            self.progTable[self.selectedSemester-1].insert(parent='', index='end', iid=self.courseTree_counter, text="",
                                   values=(subject_type + " " + catalog_type,
                                           title_type,
                                           credit_type,
                                           "Major"))

            prevcred = self.enrollCredVar.get()
            self.courseTree_counter += 1
            self.enrollCredVar.set(prevcred + int(float(credit_type)))

        dropDefault = StringVar()
        dropDefault.set("Select a semester")
        semesters = []

        for i in range(len(self.courseHist), self.progTableLength, 1):
            if i % 2 == 0:
                semesters.append("Year " + str(math.ceil(i/2)+1) + " Semester " + str(1))
            else:
                semesters.append("Year " + str(math.ceil(i/2)) + " Semester " + str(2))

        def semesterChanged(event):
            comboboxString = self.progRepoDrop.get().split()
            if comboboxString[3] == '1':
                self.selectedSemester = (int(comboboxString[1]))*2-1
            else:
                self.selectedSemester = (int(comboboxString[1]))*2

        self.subject_frame = Frame(t, borderwidth=2)
        self.subject_frame.pack(side=LEFT, anchor='n', padx=10)
        selectedSemester = ''
        self.progRepoDrop = ttk.Combobox(self.subject_frame, value=semesters, exportselection=0, width=18)
        self.progRepoDrop.pack(pady=5, anchor='n')
        self.progRepoDrop['state'] = 'readonly'
        self.progRepoDrop.bind('<<ComboboxSelected>>', semesterChanged)

        self.subject_label = Label(self.subject_frame, text="Enter a Subject",
                                   font=("Helvetica", 10), fg="black")
        self.subject_label.pack(pady=5, anchor='n')

        self.subject_example = Label(self.subject_frame, text="ex. COSC, cos",
                                     font=("Helvetica", 8), fg="grey")
        self.subject_example.pack(pady=0, anchor='n')

        subject_entry = Entry(self.subject_frame, width=25, justify=CENTER, font=("Helvetica", 10))
        subject_entry.pack(pady=10, anchor='n')

        self.catalog_label = Label(self.subject_frame, text="Enter a Catalog Number",
                                   font=("Helvetica", 8), fg="black")
        self.catalog_label.pack(pady=5, anchor='n')

        self.catalog_example = Label(self.subject_frame, text="ex. 123, 12, 1",
                                     font=("Helvetica", 8), fg="grey")
        self.catalog_example.pack(pady=0, anchor='n')

        catalog_entry = Entry(self.subject_frame, width=25, justify=CENTER, font=("Helvetica", 10))
        catalog_entry.pack(pady=10, anchor='n')

        self.title_frame = Label(self.subject_frame, text="Enter a Course Title",
                                 font=("Helvetica", 10), fg="black")
        self.title_frame.pack(pady=5, anchor='n')

        self.title_example = Label(self.subject_frame, text="ex. Computer Science I, computer sci",
                                   font=("Helvetica", 8), fg="grey")
        self.title_example.pack(pady=0, anchor='n')

        title_entry = Entry(self.subject_frame, width=25, justify=CENTER, font=("Helvetica", 10))
        title_entry.pack(pady=10, anchor='n')

        self.credit_frame = Label(self.subject_frame, text="Enter a Credit Amount",
                                  font=("Helvetica", 10), fg="black")
        self.credit_frame.pack(pady=5, anchor='n')

        self.credit_example = Label(self.subject_frame, text="ex. 4, 3.0, 2.00",
                                    font=("Helvetica", 8), fg="grey")
        self.credit_example.pack(pady=0, anchor='n')

        credit_entry = Entry(self.subject_frame, width=25, justify=CENTER, font=("Helvetica", 10))
        credit_entry.pack(pady=10, anchor='n')

        self.addButton = Button(self.subject_frame, text="Add", command=addCourse)
        self.addButton.pack(side=TOP)

        self.course_frame = Frame(t, borderwidth=2)
        self.course_frame.pack(side=RIGHT, anchor='n', padx=10)

        self.course_tree_scroll = Scrollbar(self.course_frame)
        self.course_tree_scroll.pack(side=RIGHT, fill=Y)

        self.course_tree = ttk.Treeview(self.course_frame, yscrollcommand=self.course_tree_scroll.set,
                                        column=('sub', 'cat', 'title', 'cred'), show=['headings'], height=300)
        self.course_tree.column('# 1', anchor=CENTER, width=50)
        self.course_tree.heading('# 1', text="Subject")
        self.course_tree.column('# 2', anchor=CENTER, width=50)
        self.course_tree.heading('# 2', text="Catalog")
        self.course_tree.column('# 3', anchor=CENTER, width=280)
        self.course_tree.heading('# 3', text="Title")
        self.course_tree.column('# 4', anchor=CENTER, width=50)
        self.course_tree.heading('# 4', text="Credits")

        self.course_tree.pack(pady=0)
        self.course_tree_scroll.config(command=self.course_tree.yview)

        pub.sendMessage("request_Course_by_Regex", sub="", cat="", title="", cred="")
        update_course_list(self.course_regex_list)

        self.course_tree.bind("<ButtonRelease-1>", fillout_fields)
        subject_entry.bind("<KeyRelease>", check_course)
        catalog_entry.bind("<KeyRelease>", check_course)
        title_entry.bind("<KeyRelease>", check_course)
        credit_entry.bind("<KeyRelease>", check_course)

    def planningWorksheet_layout(self):
        self.rightFrame = Frame(self.PPWFrame)
        self.rightFrame.pack(fill=BOTH)

        for i in range(4):
            self.rightFrame.columnconfigure(i, weight=1)

        pad = 10  # pady value for most frames below

        # ============================ title ============================
        ProgPlanTitle = ttk.Label(self.rightFrame, text="Program Planning Worksheet", anchor=CENTER,
                                  font=('Helvetica', 19))
        ProgPlanTitle.grid(row=0, column=0, columnspan=4, pady=20)

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

        self.editCareerButton = ttk.Button(careerFrame, text="Add/Remove", command=self.editMajorMinor)
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
        self.courseTree.column("course#", anchor=CENTER, width=90)  # anchor for the data in the column
        self.courseTree.column("title", anchor=CENTER, width=295)
        self.courseTree.column("cred", anchor=CENTER, width=35)
        self.courseTree.column("gen/elect", anchor=CENTER, width=100)

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
        self.backupCourseTree.column("course#", anchor=CENTER, width=90)
        self.backupCourseTree.column("title", anchor=CENTER, width=295)
        self.backupCourseTree.column("cred", anchor=CENTER, width=35)
        self.backupCourseTree.column("gen/elect", anchor=CENTER, width=100)

        self.backupCourseTree.heading("course#", text='Course #', anchor=CENTER)  # anchor for the title of the column
        self.backupCourseTree.heading("title", text='Title', anchor=CENTER)
        self.backupCourseTree.heading("cred", text='CR', anchor=CENTER)
        self.backupCourseTree.heading("gen/elect", text='Gen ed/Elect', anchor=CENTER)

        # ====================== memo ========================
        memoFrame = ttk.LabelFrame(self.rightFrame, text='Memo:')
        memoFrame.grid(row=16, column=0, columnspan=4, pady=pad)

        self.memoEntry = Text(memoFrame, width=50, height=5)
        self.memoEntry.pack()

        # memo_frame = Frame(self.rightFrame)
        # memo_frame.grid(row=0, column=0, sticky='w', padx=3, pady=2)
        # memoButton = Button(memo_frame, text="Memo", command=lambda: self.memoBoxOpen())
        # memoButton.pack()

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
        t.geometry("425x450")
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
                majorRemoveButton["state"] = DISABLED
                # self.selected_major_Box.bind('<FocusOut>', lambda e: self.selected_major_Box.selection_clear(0, END))

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
                minorRemoveButton["state"] = DISABLED

        def confirmSelection():
            self.setMajor_treeview()
            self.setMinor_treeview()
            self.editCareerButton.configure(state=NORMAL)
            # clear tabs from left side
            while (self.tab_parent.index("end") != 1):
                self.tab_parent.forget(self.tab_parent.index("end") - 1)
            self.FYP_refresh()
            t.destroy()

        def enableMajorRemoveBtn(e):
            majorRemoveButton["state"] = "NORMAL"

        def enableMinorRemoveBtn(e):
            minorRemoveButton["state"] = "NORMAL"

        mainframe = Frame(t)
        mainframe.pack(fill=X, ipadx=1, padx=10)

        majorframe = ttk.LabelFrame(mainframe, text="Current Major(s)")
        majorframe.pack(side=LEFT, pady=5)

        minorframe = ttk.LabelFrame(mainframe, text="Current Minor(s)")
        minorframe.pack(side=RIGHT, pady=5)

        self.selected_major_Box = Listbox(majorframe, selectmode=SINGLE, justify=CENTER, exportselection=False,
                                          height=4)
        self.selected_major_Box.pack(side=TOP)
        self.selected_major_Box.bind("<<ListboxSelect>>", enableMajorRemoveBtn)

        self.selected_minor_Box = Listbox(minorframe, selectmode=SINGLE, justify=CENTER, exportselection=False,
                                          height=4)
        self.selected_minor_Box.pack(side=TOP)
        self.selected_minor_Box.bind("<<ListboxSelect>>", enableMinorRemoveBtn)

        majorRemoveButton = ttk.Button(majorframe, text="Remove", command=removeMajor, state=DISABLED)
        majorRemoveButton.pack()

        minorRemoveButton = ttk.Button(minorframe, text="Remove", command=removeMinor, state=DISABLED)
        minorRemoveButton.pack()

        label3 = Label(majorframe, text="Major(s)")
        label3.pack(side=TOP)
        label4 = Label(minorframe, text="Minor(s)")
        label4.pack(side=TOP)

        self.schCbox1 = ttk.Combobox(majorframe, value=self.schList, exportselection=0, width=18)
        self.schCbox1.pack(side=TOP)
        self.schCbox1.bind("<<ComboboxSelected>>", self.getMajorBySchool)

        self.schCbox2 = ttk.Combobox(minorframe, value=self.schList, exportselection=0, width=18)
        self.schCbox2.pack(side=TOP)
        self.schCbox2.bind("<<ComboboxSelected>>", self.getMinorBySchool)

        self.majorVar = StringVar()
        self.majorBox = Listbox(majorframe, selectmode=SINGLE, justify=CENTER, listvariable=self.majorVar,
                                exportselection=False, height=8)
        # export selection allows us to work on other listbox while not calling this binding
        self.majorBox.pack(side=TOP)
        self.majorBox.bind('<Double-1>', majorSelection)  # double-click binding

        self.minorVar = StringVar()
        self.minorBox = Listbox(minorframe, selectmode=SINGLE, justify=CENTER, listvariable=self.minorVar,
                                exportselection=False, height=8)
        self.minorBox.pack(side=TOP)
        self.minorBox.bind('<Double-1>', minorSelection)

        # for if major & minor treeview were already filled
        for id in self.majorTree.get_children():
            major = self.majorTree.item(id)['text']
            self.selected_major_Box.insert(END, major)

        for id in self.minorTree.get_children():
            minor = self.minorTree.item(id)['text']
            self.selected_minor_Box.insert(END, minor)

        comfirmButton = ttk.Button(t, text="Save", command=confirmSelection)
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

    def FYP_refresh(self):
        majors, minors = [], []
        for id in self.majorTree.get_children():
            majors.append(self.majorTree.item(id)['text'])
        for id in self.minorTree.get_children():
            minors.append(self.minorTree.item(id)['text'])
        pub.sendMessage("refresh_fyp", majors=majors, minors=minors)

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
        t.geometry("700x400")
        t.resizable(width=FALSE, height=FALSE)
        t.transient(self.mainwin)
        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')

        def close(e):
            self.addCourseButton.configure(state=NORMAL)
            t.destroy()

        t.bind('<Destroy>', close)
        self.addCourseButton.configure(state=DISABLED)

        def update_course_list(data):
            for i in self.course_tree.get_children():
                self.course_tree.delete(i)

            #self.course_tree.tag_configure('evenrow', background="grey")
            #self.course_tree.tag_configure('oddrow', background="white")

            for item in data:
                self.course_tree.insert('', 'end',
                                   values=(item['Subject'], item['Catalog'], item['Long Title'], item['Allowd Unt']))

        def fillout_fields(event):
            subject_entry.delete(0, END)
            catalog_entry.delete(0, END)
            title_entry.delete(0, END)
            credit_entry.delete(0, END)

            course = self.course_tree.focus()
            course_info = self.course_tree.item(course)['values']

            subject_entry.insert(0, course_info[0])
            catalog_entry.insert(0, course_info[1])
            title_entry.insert(0, course_info[2])
            credit_entry.insert(0, course_info[3])

        def check_course(event):
            subject_type = subject_entry.get().upper()
            catalog_type = catalog_entry.get()
            title_type = title_entry.get().upper()
            credit_type = credit_entry.get()

            pub.sendMessage("request_Course_by_Regex", sub=subject_type, cat=catalog_type, title=title_type, cred=credit_type)
            update_course_list(self.course_regex_list)

        # adds searched course into the treeview
        def addCourse():
            subject_type = subject_entry.get().upper()
            catalog_type = catalog_entry.get()
            title_type = title_entry.get().upper()
            credit_type = credit_entry.get()
            self.courseTree.insert(parent='', index='end', iid=self.courseTree_counter, text="",
                                   values=(subject_type + " " + catalog_type,
                                           title_type,
                                           credit_type,
                                           "Major"))

            prevcred = self.enrollCredVar.get()
            self.courseTree_counter += 1
            self.enrollCredVar.set(prevcred + int(float(credit_type)))

        self.subject_frame = Frame(t, borderwidth=2)
        self.subject_frame.pack(side=LEFT, anchor='n', padx=10)

        self.subject_label = Label(self.subject_frame, text="Enter a Subject",
                                   font=("Helvetica", 10), fg="black")
        self.subject_label.pack(pady=5, anchor='n')

        self.subject_example = Label(self.subject_frame, text="ex. COSC, cos",
                                     font=("Helvetica", 8), fg="grey")
        self.subject_example.pack(pady=0, anchor='n')

        subject_entry = Entry(self.subject_frame, width=25, justify=CENTER, font=("Helvetica", 10))
        subject_entry.pack(pady=10, anchor='n')

        self.catalog_label = Label(self.subject_frame, text="Enter a Catalog Number",
                                   font=("Helvetica", 8), fg="black")
        self.catalog_label.pack(pady=5, anchor='n')

        self.catalog_example = Label(self.subject_frame, text="ex. 123, 12, 1",
                                     font=("Helvetica", 8), fg="grey")
        self.catalog_example.pack(pady=0, anchor='n')

        catalog_entry = Entry(self.subject_frame, width=25, justify=CENTER, font=("Helvetica", 10))
        catalog_entry.pack(pady=10, anchor='n')

        self.title_frame = Label(self.subject_frame, text="Enter a Course Title",
                                 font=("Helvetica", 10), fg="black")
        self.title_frame.pack(pady=5, anchor='n')

        self.title_example = Label(self.subject_frame, text="ex. Computer Science I, computer sci",
                                   font=("Helvetica", 8), fg="grey")
        self.title_example.pack(pady=0, anchor='n')

        title_entry = Entry(self.subject_frame, width=25, justify=CENTER, font=("Helvetica", 10))
        title_entry.pack(pady=10, anchor='n')

        self.credit_frame = Label(self.subject_frame, text="Enter a Credit Amount",
                                  font=("Helvetica", 10), fg="black")
        self.credit_frame.pack(pady=5, anchor='n')

        self.credit_example = Label(self.subject_frame, text="ex. 4, 3.0, 2.00",
                                    font=("Helvetica", 8), fg="grey")
        self.credit_example.pack(pady=0, anchor='n')

        credit_entry = Entry(self.subject_frame, width=25, justify=CENTER, font=("Helvetica", 10))
        credit_entry.pack(pady=10, anchor='n')


        self.addButton = Button(self.subject_frame, text="Add", command=addCourse)
        self.addButton.pack(side=TOP)

        self.course_frame = Frame(t, borderwidth=2)
        self.course_frame.pack(side=RIGHT, anchor='n', padx=10)

        self.course_tree_scroll = Scrollbar(self.course_frame)
        self.course_tree_scroll.pack(side=RIGHT, fill=Y)


        self.course_tree = ttk.Treeview(self.course_frame, yscrollcommand=self.course_tree_scroll.set,
                                        column=('sub', 'cat', 'title', 'cred'), show=['headings'], height=300)
        self.course_tree.column('# 1', anchor=CENTER, width=50)
        self.course_tree.heading('# 1', text="Subject")
        self.course_tree.column('# 2', anchor=CENTER, width=50)
        self.course_tree.heading('# 2', text="Catalog")
        self.course_tree.column('# 3', anchor=CENTER, width=280)
        self.course_tree.heading('# 3', text="Title")
        self.course_tree.column('# 4', anchor=CENTER, width=50)
        self.course_tree.heading('# 4', text="Credits")

        self.course_tree.pack(pady=0)
        self.course_tree_scroll.config(command=self.course_tree.yview)

        pub.sendMessage("request_Course_by_Regex", sub="", cat="", title="", cred="")
        update_course_list(self.course_regex_list)

        self.course_tree.bind("<ButtonRelease-1>", fillout_fields)
        subject_entry.bind("<KeyRelease>", check_course)
        catalog_entry.bind("<KeyRelease>", check_course)
        title_entry.bind("<KeyRelease>", check_course)
        credit_entry.bind("<KeyRelease>", check_course)


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
        t.wm_title("Search for Course")
        t.geometry("700x400")
        t.resizable(width=FALSE, height=FALSE)
        t.transient(self.mainwin)
        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')

        def close(e):
            self.addBackupButton.configure(state=NORMAL)
            t.destroy()

        t.bind('<Destroy>', close)
        self.addBackupButton.configure(state=DISABLED)

        def backup_update_course_list(data):
            for i in self.backup_addCourseTree.get_children():
                self.backup_addCourseTree.delete(i)

            # self.course_tree.tag_configure('evenrow', background="grey")
            # self.course_tree.tag_configure('oddrow', background="white")

            for item in data:
                self.backup_addCourseTree.insert('', 'end',
                                        values=(
                                        item['Subject'], item['Catalog'], item['Long Title'], item['Allowd Unt']))

        def fillout_fields(event):
            subject_entry.delete(0, END)
            catalog_entry.delete(0, END)
            title_entry.delete(0, END)
            credit_entry.delete(0, END)

            course = self.backup_addCourseTree.focus()
            course_info = self.backup_addCourseTree.item(course)['values']

            subject_entry.insert(0, course_info[0])
            catalog_entry.insert(0, course_info[1])
            title_entry.insert(0, course_info[2])
            credit_entry.insert(0, course_info[3])

        def check_course(event):
            subject_type = subject_entry.get().upper()
            catalog_type = catalog_entry.get()
            title_type = title_entry.get().upper()
            credit_type = credit_entry.get()

            pub.sendMessage("request_Backup_Course_by_Regex", sub=subject_type, cat=catalog_type, title=title_type,
                            cred=credit_type)

            backup_update_course_list(self.backup_course_regex_list)

        # adds searched course into the treeview
        def backup_addCourse():
            subject_type = subject_entry.get().upper()
            catalog_type = catalog_entry.get()
            title_type = title_entry.get().upper()
            credit_type = credit_entry.get()
            print(subject_type)
            self.backupCourseTree.insert(parent='', index='end', iid=self.backupCourseTree_counter, text="",
                                   values=(subject_type + " " + catalog_type,
                                           title_type,
                                           credit_type,
                                           "Major"))

            prevcred = self.enrollCredVar.get()
            self.backupCourseTree_counter += 1
            self.enrollCredVar.set(prevcred + int(float(credit_type)))

        self.backup_subject_frame = Frame(t, borderwidth=2)
        self.backup_subject_frame.pack(side=LEFT, anchor='n', padx=10)

        self.subject_label = Label(self.backup_subject_frame, text="Enter a Subject",
                                   font=("Helvetica", 10), fg="black")
        self.subject_label.pack(pady=5, anchor='n')

        self.subject_example = Label(self.backup_subject_frame, text="ex. COSC, cos",
                                     font=("Helvetica", 8), fg="grey")
        self.subject_example.pack(pady=0, anchor='n')

        subject_entry = Entry(self.backup_subject_frame, width=25, justify=CENTER, font=("Helvetica", 10))
        subject_entry.pack(pady=10, anchor='n')

        self.catalog_label = Label(self.backup_subject_frame, text="Enter a Catalog Number",
                                   font=("Helvetica", 8), fg="black")
        self.catalog_label.pack(pady=5, anchor='n')

        self.catalog_example = Label(self.backup_subject_frame, text="ex. 123, 12, 1",
                                     font=("Helvetica", 8), fg="grey")
        self.catalog_example.pack(pady=0, anchor='n')

        catalog_entry = Entry(self.backup_subject_frame, width=25, justify=CENTER, font=("Helvetica", 10))
        catalog_entry.pack(pady=10, anchor='n')

        self.title_frame = Label(self.backup_subject_frame, text="Enter a Course Title",
                                 font=("Helvetica", 10), fg="black")
        self.title_frame.pack(pady=5, anchor='n')

        self.title_example = Label(self.backup_subject_frame, text="ex. Computer Science I, computer sci",
                                   font=("Helvetica", 8), fg="grey")
        self.title_example.pack(pady=0, anchor='n')

        title_entry = Entry(self.backup_subject_frame, width=25, justify=CENTER, font=("Helvetica", 10))
        title_entry.pack(pady=10, anchor='n')

        self.credit_frame = Label(self.backup_subject_frame, text="Enter a Credit Amount",
                                  font=("Helvetica", 10), fg="black")
        self.credit_frame.pack(pady=5, anchor='n')

        self.credit_example = Label(self.backup_subject_frame, text="ex. 4, 3.0, 2.00",
                                    font=("Helvetica", 8), fg="grey")
        self.credit_example.pack(pady=0, anchor='n')

        credit_entry = Entry(self.backup_subject_frame, width=25, justify=CENTER, font=("Helvetica", 10))
        credit_entry.pack(pady=10, anchor='n')

        self.addButton = Button(self.backup_subject_frame, text="Add", command=backup_addCourse)
        self.addButton.pack(side=TOP)

        self.course_frame = Frame(t, borderwidth=2)
        self.course_frame.pack(side=RIGHT, anchor='n', padx=10)

        self.backup_course_tree_scroll = Scrollbar(self.course_frame)
        self.backup_course_tree_scroll.pack(side=RIGHT, fill=Y)

        self.backup_addCourseTree = ttk.Treeview(self.course_frame, yscrollcommand=self.backup_course_tree_scroll.set,
                                        column=('sub', 'cat', 'title', 'cred'), show=['headings'], height=300)
        self.backup_addCourseTree.column('# 1', anchor=CENTER, width=50)
        self.backup_addCourseTree.heading('# 1', text="Subject")
        self.backup_addCourseTree.column('# 2', anchor=CENTER, width=50)
        self.backup_addCourseTree.heading('# 2', text="Catalog")
        self.backup_addCourseTree.column('# 3', anchor=CENTER, width=280)
        self.backup_addCourseTree.heading('# 3', text="Title")
        self.backup_addCourseTree.column('# 4', anchor=CENTER, width=50)
        self.backup_addCourseTree.heading('# 4', text="Credits")

        self.backup_addCourseTree.pack(pady=0)
        self.backup_course_tree_scroll.config(command=self.backup_addCourseTree.yview)

        pub.sendMessage("request_Backup_Course_by_Regex", sub="", cat="", title="",
                        cred="")
        backup_update_course_list(self.backup_course_regex_list)

        self.backup_addCourseTree.bind("<ButtonRelease-1>", fillout_fields)
        subject_entry.bind("<KeyRelease>", check_course)
        catalog_entry.bind("<KeyRelease>", check_course)
        title_entry.bind("<KeyRelease>", check_course)
        credit_entry.bind("<KeyRelease>", check_course)

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

    def planningWorksheet_fill(self, obj, tcred, courses, numbCourse, major, minor, bcourses,
                               courseHist, fourYear, minorFourYear, minorReqList, policies,
                               sumCourse, winCourse):
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

    # def memoBoxOpen(self):
    #     self.pop = Toplevel(self.rightFrame)
    #     self.pop.title("Student Memo")
    #     self.pop.geometry("490x150")
    #     self.pop.config(bg="white")
    #
    #     memoFrame = ttk.LabelFrame(self.pop, text='Memo:')
    #     memoFrame.grid(row=16, column=0, columnspan=4, pady=10)
    #
    #     self.memoEntry = Text(memoFrame, width=60, height=7)
    #     self.memoEntry.pack()
    #
    #     self.memoEntry.delete('1.0', 'end')
    #     self.memoEntry.insert('1.0', self.memo_to_display)

    def univ_policy_box(self):
        self.pop = Toplevel(self.innerLeftFrame)
        self.pop.title("University Policies")
        self.pop.geometry("720x360")
        self.pop.config(bg="white")

        # ============================ Policy Memo ============================
        policyFrame = ttk.LabelFrame(self.pop, height=200, width=self.left_width,
                                     text='University Policy:')
        policyFrame.pack(pady=30)

        self.policyMemoEntry = Text(policyFrame, width=90, height=10)
        self.policyMemoEntry.pack()

        self.policyMemoEntry.config(state=NORMAL)
        self.policyMemoEntry.delete('1.0', 'end')
        self.policyMemoEntry.insert('1.0', self.policy_to_display)
        self.policyMemoEntry.config(state=DISABLED)

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
        menu.add_cascade(label='Student', menu=self.schedule)
        self.scheduleMenu()

        load = Menu(menu, tearoff=0)
        menu.add_cascade(label='View    ', menu=load)
        self.loadMenu(load)

        # DataBase
        self.DB = Menu(menu, tearoff=0)
        menu.add_cascade(label='Update DB', menu=self.DB)
        self.DataBaseMenu()

        self.helpmenu = Menu(menu, tearoff=0)
        menu.add_cascade(label='Help ', menu=self.helpmenu)
        self.helpmenu.add_command(label="Help Menu", command=self.printHelp)

    # schedule menu dropdown
    def scheduleMenu(self):
        self.schedule.add_command(label='New', command=self.newSchedule)
        self.schedule.add_command(label='Open...', command=self.openSchedule)
        self.schedule.add_separator()
        self.schedule.add_command(label='Save', command=self.saveSchedule)
        self.schedule.add_separator()
        self.schedule.add_command(label='Export', command=self.exportSchedule)
        self.schedule.add_command(label='Print', command=self.printSchedule)

    def printHelp(self):

        # Create pop up window on top level of application
        t = Toplevel(self.mainwin)
        t.wm_title("Help Menu")
        t.geometry("1000x600")
        t.attributes('-topmost', 'true')

        top = Frame(t)  # Top frame for title and buttons
        bottom = Frame(t)  # Bottom frame for list box containing help menu
        top.pack(side=TOP)
        bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

        # Create scroll bar
        scrollbar = Scrollbar(bottom)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Create list box in bottom frame for help menu
        helpmenu = Listbox(bottom, yscrollcommand=scrollbar.set)
        helpmenu.pack(side=LEFT, fill=BOTH, expand=YES)

        # Displays the menu options
        def menu_option():
            helpmenu.delete(0, 'end')
            file = open('Help/help.txt')
            for i in file:
                helpmenu.insert(END, str(i))

        # Displays the four year plan options
        def four_option():
            helpmenu.delete(0, 'end')
            file = open('Help/help2.txt')
            for i in file:
                helpmenu.insert(END, str(i))

        # Displays the program planning options
        def program_option():
            helpmenu.delete(0, 'end')
            file = open('Help/help3.txt')
            for i in file:
                helpmenu.insert(END, str(i))

        menu_option()  # Starts on first page of help menu
        head = Label(top, text="Help Menu", font=125)  # Title
        head.pack()
        button1 = Button(top, text="Menu Options", width=15, height=1, command=menu_option)  # Button for menu options
        button1.pack(in_=top, side=LEFT)
        button2 = Button(top, text="Four Year Plan", width=15, height=1,
                         command=four_option)  # Button for four year options
        button2.pack(in_=top, side=LEFT)
        button3 = Button(top, text="Program Planning", width=15, height=1,
                         command=program_option)  # Button for program planning options
        button3.pack(in_=top, side=LEFT)

        scrollbar.config(command=helpmenu.yview)  # Set scroll bar to effect Y axis view of list box

    def newSchedule(self):
        self.planningWorksheet_reset()
        self.FYP_reset()
        self.courseTakenList_reset()
        # Removes buttons when student information is not present
        self.addProgRepoBtn.grid_forget()
        self.removeProgRepoBtn.grid_forget()

    def openSchedule(self):
        pub.sendMessage("requestStudents")

        t = Toplevel(self.mainwin)
        t.wm_title("Search for Student")
        t.geometry("440x350")
        t.resizable(width=0, height=0)
        t.attributes('-topmost', 'true')
        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')

        def openScheduleSearchButton(e):
            if self.studentBox.curselection() != "":
                selectedStudent = self.studentBox.get(self.studentBox.curselection())
                selectedStudentSplit = selectedStudent.split()

                fname.delete(0, END)
                lname.delete(0, END)
                idE.delete(0, END)

                fname.insert(0, selectedStudentSplit[0])
                lname.insert(0, selectedStudentSplit[1])
                idE.insert(0, selectedStudentSplit[2])

                name = fname.get() + " " + lname.get()
                id = idE.get()

                if name != "" and id != "":
                    self.studentBox.delete(0, END)
                    pub.sendMessage("request_PPW", name=name, id=int(id))
                    self.schedule.entryconfigure(1, state=NORMAL)
                    t.destroy()
                    # Shows buttons for Progress Report when student information is present
                    self.addProgRepoBtn.grid(column=0, row=0, sticky=E, padx=120)
                    self.removeProgRepoBtn.grid(column=0, row=0, sticky=E, padx=25)


        def filtr(e):
            chars1 = fname.get()
            chars2 = lname.get()
            chars3 = idE.get()
            index = 0
            if chars1 or chars2 or chars3 != "":
                fltrdStu1 = [x for x in self.students if chars1.lower() in x.lower()]
                fltrdStu1 = [x for x in fltrdStu1 if chars2.lower() in x.lower()]
                fltrdStu1 = [x for x in fltrdStu1 if chars3.lower() in x.lower()]
                self.studentBox.delete(0, END)
                fltrdStu = list(fltrdStu1)

                for i in fltrdStu:
                    self.studentBox.insert(END, fltrdStu[index])
                    index += 1
            else:
                self.studentBox.delete(0, END)
                for i in self.students:
                    self.studentBox.insert(END, self.students[index])
                    index += 1

        def fillEntry(e):
            if self.studentBox.curselection() != "":
                selectedStudent = self.studentBox.get(self.studentBox.curselection())
                selectedStudentSplit = selectedStudent.split()

                fname.delete(0, END)
                lname.delete(0, END)
                idE.delete(0, END)

                fname.insert(0, selectedStudentSplit[0])
                lname.insert(0, selectedStudentSplit[1])
                idE.insert(0, selectedStudentSplit[2])

        def close(e):
            self.schedule.entryconfigure(1, state=NORMAL)
            t.destroy()

        t.bind('<Destroy>', close)
        self.schedule.entryconfigure(1, state=DISABLED)

        nameFrame = Frame(t)
        nameFrame.pack(side=TOP, anchor='w', padx=20, pady=10)

        idFrame = Frame(t)
        idFrame.pack(side=TOP, anchor='w', padx=130)

        butFrame = Frame(t)
        butFrame.pack(side=BOTTOM, anchor=CENTER, pady=10)

        label2 = Label(nameFrame, text='First name:').pack(side=LEFT)
        fname = ttk.Entry(nameFrame, width=10)
        fname.pack(side=LEFT)
        fname.bind("<KeyRelease>", filtr)

        lname = ttk.Entry(nameFrame, width=15)
        lname.pack(side=RIGHT)
        label3 = Label(nameFrame, text='Last name:').pack(side=RIGHT)
        lname.bind("<KeyRelease>", filtr)

        label3 = Label(idFrame, text='Student Id:').pack(side=LEFT)
        idE = ttk.Entry(idFrame, width=10)
        idE.pack(side=LEFT)
        idE.bind("<KeyRelease>", filtr)

        searchB = Button(butFrame, text='Open')
        searchB.pack()
        searchB.bind("<ButtonRelease>", openScheduleSearchButton)

        mainframe = Frame(t)
        mainframe.pack(fill=X, ipadx=1, padx=100, pady=10)

        studentFrame = ttk.LabelFrame(mainframe, text="Students")
        studentFrame.pack(side=TOP, anchor=CENTER)

        self.studentBox = Listbox(studentFrame, selectmode=SINGLE, justify=CENTER, exportselection=False,
                                  listvariable=self.studentsVar, height=10, width=3500, font=('Helvetica', 12))
        self.studentBox.pack(side=TOP)
        self.studentBox.bind("<Double-Button-1>", openScheduleSearchButton)
        self.studentBox.bind("<<ListboxSelect>>", fillEntry)
        self.studentBox.delete(0, END)
        self.students = []

        for i in self.studentsVar:
            self.students.append(str(self.studentsVar[i]["name"]) + " " + str(self.studentsVar[i]["s_id"]))
        self.students.sort()
        index = 0
        for i in self.students:
            self.studentBox.insert(END, self.students[index])
            index += 1

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
        fnameE = "{}.pdf".format(self.nameEntry.get())
        pub.sendMessage("export_schedule", id=self.idEntry.get(), fname=fnameE)

    def printSchedule(self):
        print("Print schedule")

    def loadMenu(self, major):
        major.add_command(label='Four Year Plan', command=self.showFourYearPlan)
        major.add_command(label='Course Taken List', command=self.showCourseTakenList)

    def showFourYearPlan(self):
        self.courseTakenListFrame.pack_forget()
        self.PPWFrame.pack_forget()
        self.leftFrame.pack(side=LEFT, fill=Y, padx=5)
        self.PPWFrame.pack(side=RIGHT, fill=Y)
        self.PPWFrame.pack_propagate(0)

    def showCourseTakenList(self):
        self.leftFrame.pack_forget()
        self.courseTakenListFrame.pack(side=LEFT, fill=Y, padx=5)
        self.courseTakenListFrame['width'] = self.left_width
        self.courseTakenListFrame.propagate(0)

    def openCSV(self):
        pub.sendMessage("request_CSV")

    def close(self, window):
        window.destroy()

    def openMajorButton(self, major):
        if self.majorBox.get(self.majorBox.curselection()) != "":
            self.close(self.addEditMajorWindow)
            pub.sendMessage("request_MajorsFYP", major=major)
            self.schedule.entryconfigure(1, state=NORMAL)

            self.editMajorWindow = Toplevel(self.mainwin)
            self.editMajorWindow.geometry("1150x850")
            self.editMajorWindow.wm_title("Edit Major")
            self.editMajorWindow.attributes('-topmost', 'true')
        else:
            return

        treeviewFrame = Frame(self.editMajorWindow)
        treeviewFrame.pack(fill=BOTH, expand=True)
        addCrsBtnFrame = Frame(self.editMajorWindow)
        addCrsBtnFrame.pack()

        edtMjLbls = []
        edtMjTbls = []

        addCourseBtn = Button(addCrsBtnFrame, text="Add course", command=lambda: self.FYP_addCourseButton(self.editMajorWindow))
        rmvCourseBtn = Button(addCrsBtnFrame, text="Remove course", command=lambda: self.FYP_delCourseButton(self.editMajorWindow))
        addCourseBtn.pack(side=LEFT, padx=10)
        rmvCourseBtn.pack(side=RIGHT)

        # Treeviews are created
        self.createTable(treeviewFrame, edtMjLbls, edtMjTbls, 8)

        # Filling semesters for major
        semsIndex = 0
        for sem in self.majorsFYP:
            edtMjTbls_iid = 0
            for course in sem:
                edtMjTbls[semsIndex].insert(parent='', index='end',
                                                              iid=edtMjTbls_iid,
                                                              values=(course[1] + course[2], course[3], course[4]))
                edtMjTbls_iid += 1
            semsIndex += 1
        # ============================ Add Semester Table Button ============================
        """
        self.addSemesterBtn = Button(self.semesterFrame, text="Add a semester")
        self.addSemesterBtn.pack()
        self.addSemesterBtn.place(x=120, y=950)
        self.temp = semesterCounter
        self.tempY = yPos
        self.addSemesterBtn['command'] = lambda: self.createSemesterBtn("Extra Semester", self.tempY, self.semTable,
                                                                        self.semLabel, self.semesterFrame, self.temp)
        """


    # Add Major Button from Update DB
    def addEditMajor(self):
        self.addEditMajorWindow = Toplevel(self.mainwin)
        self.addEditMajorWindow.wm_title("Edit/Add Major")
        self.addEditMajorWindow.geometry("300x310")
        self.addEditMajorWindow.resizable(width=0, height=0)
        self.addEditMajorWindow.attributes('-topmost', 'true')
        self.mainwin.eval(f'tk::PlaceWindow {str(self.addEditMajorWindow)} center')
        pub.sendMessage("request_Majors")  # Retrieves list of majors from database
        self.majors.sort()

        def filtr(e):
            chars = majorEntry.get()

            index = 0
            if chars != "":
                fltrdStu1 = [x for x in self.majors if chars.lower() in x.lower()]
                self.majorBox.delete(0, END)
                fltrdStu = list(fltrdStu1)

                for i in fltrdStu:
                    self.majorBox.insert(END, fltrdStu[index])
                    index += 1
            else:
                self.majorBox.delete(0, END)
                for i in self.majors:
                    self.majorBox.insert(END, self.majors[index])
                    index += 1

        majorFrame = Frame(self.addEditMajorWindow)
        majorFrame.pack(padx=50, pady=10)

        majorBoxFrame = Frame(self.addEditMajorWindow)
        majorBoxFrame.pack(ipady=10)

        btnFrame = Frame(self.addEditMajorWindow)
        btnFrame.pack()

        majorEntryLbl = Label(majorFrame, text='Major:')
        majorEntryLbl.pack(side=LEFT)
        majorEntry = ttk.Entry(majorFrame, width=200)
        majorEntry.pack(side=LEFT)
        majorEntry.bind("<KeyRelease>", filtr)

        self.majorBox = Listbox(majorBoxFrame, selectmode=SINGLE, justify=CENTER, exportselection=False,
                                listvariable=self.majors, height=10, width=30, font=('Helvetica', 12))
        self.majorBox.pack(side=TOP)
        self.majorBox.delete(0, END)

        index = 0
        for i in self.majors:
            self.majorBox.insert(END, self.majors[index])
            index += 1

        searchB = Button(btnFrame, text='Open', command=lambda: self.openMajorButton(self.majorBox.get(self.majorBox.curselection())))
        searchB.pack()
        """
        self.frame.bind("<Return>",
                        lambda event, a=10, b=20, c=30:
                        self.rand_func(a, b, c))
        """
    def openMinorButton(self):
        if self.minorBox.get(self.minorBox.curselection()) != "":
            self.close(self.addEditMinorWindow)
            #pub.sendMessage("request_PPW", name=name, id=int(id))
            self.schedule.entryconfigure(1, state=NORMAL)

            editMinorWindow = Toplevel(self.mainwin)
            editMinorWindow.wm_title("Edit Minor")
            editMinorWindow.geometry("1150x800")
            editMinorWindow.resizable(width=0, height=0)
            editMinorWindow.attributes('-topmost', 'true')
        else:
            return

        editMinorFrame = Frame(editMinorWindow)
        editMinorFrame.pack(fill=BOTH, expand=True)

        edtMiLbls = []
        edtMiTbls = []

        # Treeviews are created
        self.createTable(editMinorFrame, edtMiLbls, edtMiTbls, 8)

    # Add minor button in Update DB
    def addEditMinor(self):
        self.addEditMinorWindow = Toplevel(self.mainwin)
        self.addEditMinorWindow.wm_title("Edit/Add Minor")
        self.addEditMinorWindow.geometry("300x310")
        self.addEditMinorWindow.resizable(width=0, height=0)
        self.addEditMinorWindow.attributes('-topmost', 'true')
        self.mainwin.eval(f'tk::PlaceWindow {str(self.addEditMinorWindow)} center')
        pub.sendMessage("request_Minors")  # Retrieves list of majors from database
        self.minors.sort()

        def filtr(e):
            chars = minorEntry.get()

            index = 0
            if chars != "":
                fltrdStu1 = [x for x in self.minors if chars in x]
                self.minorBox.delete(0, END)
                fltrdStu = list(fltrdStu1)

                for i in fltrdStu:
                    self.minorBox.insert(END, fltrdStu[index])
                    index += 1
            else:
                self.minorBox.delete(0, END)
                for i in self.minors:
                    self.minorBox.insert(END, self.minors[index])
                    index += 1

        minorFrame = Frame(self.addEditMinorWindow)
        minorFrame.pack(padx=50, pady=10)

        minorBoxFrame = Frame(self.addEditMinorWindow)
        minorBoxFrame.pack(ipady=10)

        btnFrame = Frame(self.addEditMinorWindow)
        btnFrame.pack()

        minorEntryLbl = Label(minorFrame, text='Major:')
        minorEntryLbl.pack(side=LEFT)
        minorEntry = ttk.Entry(minorFrame, width=200)
        minorEntry.pack(side=LEFT)
        minorEntry.bind("<KeyRelease>", filtr)

        self.minorBox = Listbox(minorBoxFrame, selectmode=SINGLE, justify=CENTER, exportselection=False,
                                listvariable=self.minors, height=10, width=30, font=('Helvetica', 12))
        self.minorBox.pack(side=TOP)
        self.minorBox.delete(0, END)

        index = 0
        for i in self.minors:
            self.minorBox.insert(END, self.minors[index])
            index += 1

        searchB = Button(btnFrame, text='Open', command=self.openMinorButton)
        searchB.pack()

    # Delete major in Update DB
    def delMajor(self):
        t = Toplevel(self.mainwin)
        t.wm_title("Delete Major")
        t.geometry("350x125")
        t.resizable(width=0, height=0)
        t.attributes('-topmost', 'true')
        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')

        def close(e):
            self.DB.entryconfigure(5, state=NORMAL)
            t.destroy()

        t.bind('<Destroy>', close)
        self.DB.entryconfigure(5, state=DISABLED)

        def deleteMajorButton():  # Delete the major from database
            name = fnameE.get()
            if name != "" and id != "":
                pub.sendMessage("request_DelMajor", acad=name)
                self.DB.entryconfigure(5, state=NORMAL)
                t.destroy()

        nameFrame = Frame(t)
        nameFrame.pack(side=TOP, anchor='w', padx=20, pady=10)

        butFrame = Frame(t)
        butFrame.pack(side=BOTTOM, anchor=CENTER, pady=10)

        label2 = Label(nameFrame, text='Major Abbreviation:').pack(side=LEFT)
        fnameE = ttk.Entry(nameFrame, width=15)
        fnameE.pack(side=LEFT)

        searchB = Button(butFrame, text='Delete', command=deleteMajorButton)
        searchB.pack()

    # Delete Minor in Update DB
    def delMinor(self):
        t = Toplevel(self.mainwin)
        t.wm_title("Delete Minor")
        t.geometry("300x125")
        t.resizable(width=0, height=0)
        t.attributes('-topmost', 'true')
        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')

        def close(e):
            self.DB.entryconfigure(6, state=NORMAL)
            t.destroy()

        t.bind('<Destroy>', close)
        self.DB.entryconfigure(6, state=DISABLED)

        def deleteMinorButton():  # Delete the minor from database
            name = fnameE.get()
            if name != "" and id != "":
                pub.sendMessage("request_DelMinor", acad=name)
                self.DB.entryconfigure(6, state=NORMAL)
                t.destroy()

        nameFrame = Frame(t)
        nameFrame.pack(side=TOP, anchor='w', padx=20, pady=10)

        butFrame = Frame(t)
        butFrame.pack(side=BOTTOM, anchor=CENTER, pady=10)

        label2 = Label(nameFrame, text='Minor Abbreviation:').pack(side=LEFT)
        fnameE = ttk.Entry(nameFrame, width=10)
        fnameE.pack(side=LEFT)

        searchB = Button(butFrame, text='Delete', command=deleteMinorButton)
        searchB.pack()

    # data base menu dropdown
    def DataBaseMenu(self):
        self.DB.add_command(label='Current Semester Course', command=self.openCSV)
        self.DB.add_separator()
        self.DB.add_command(label='Edit/Add Major', command=self.addEditMajor)
        self.DB.add_command(label='Edit/Add Minor', command=self.addEditMinor)
        self.DB.add_separator()
        self.DB.add_command(label='Delete Major', command=self.delMajor)
        self.DB.add_command(label='Delete Minor', command=self.delMinor)
