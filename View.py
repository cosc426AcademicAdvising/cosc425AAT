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
from ttkbootstrap import Style, Colors
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

        self.TVstyle = Style()
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
        self.majors = []  # Holds major abbreviations
        self.minors = []  # Holds minor abbreviations
        self.majorsFYP = []  # Holds Four Year Plan for Major
        self.minorsFYP = []  # Holds Four Year Plan for Minor
        self.minorsReqs = [] # Holds Minor Pre-Requisites
        self.selectedSemester = 0 # Selected semester
        self.tot_Removed = 0

        self.loginPage()  # Calls login page function
        self.menuBar()  # Calls menu bar function
        self.loginWindow.protocol("WM_DELETE_WINDOW",
                                  self.login_closing)  # If user closes login window application closes
        style = Style() # Creates Style object
        style.theme_use("sutheme")  # Sets the of application using the style object

    # Prompt message before closing program,
    # Also closes all TopLevel functions
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            for widget in self.mainwin.winfo_children():
                if isinstance(widget, Toplevel):
                    widget.destroy()
            self.mainwin.destroy()

    # Used to close login window
    def login_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?", parent=self.loginWindow):
            for widget in self.mainwin.winfo_children():
                if isinstance(widget, Toplevel):
                    widget.destroy()
            self.loginWindow.destroy()
            self.mainwin.destroy()

    # Creates the main application window for GUI
    def layout(self):
        # Establishes the screenwidth for application window
        self.right_width = self.mainwin.winfo_screenwidth() * 0.4
        self.left_width = self.mainwin.winfo_screenwidth() - self.right_width

        self.mainFrame = Frame(self.mainwin)
        self.mainFrame.pack(fill=BOTH, padx=10, pady=10, expand=1, ipadx=10)

        # Program is split into two frames leftFrame and PPWFrame
        # four year plan
        self.leftFrame = Frame(self.mainFrame, width=self.left_width, borderwidth=2, relief=GROOVE)
        self.leftFrame.pack(side=LEFT, fill=Y, padx=5)

        # program planning worksheet
        self.PPWFrame = Frame(self.mainFrame, width=self.right_width, borderwidth=2, relief=GROOVE)
        self.PPWFrame.pack(side=RIGHT, fill=Y)
        self.PPWFrame.pack_propagate(0)

        # Frame for course taken treeview
        self.courseTakenListFrame = Frame(self.mainFrame, width=self.left_width, borderwidth=2, relief=GROOVE)
        self.courseTakenListFrame.pack(side=LEFT, fill=Y, padx=5)
        self.courseTakenListFrame.pack_forget()  # hide frame

        # Functions for creating more GUI components
        self.FourYearPlan()
        self.planningWorksheet_layout()
        self.courseTakenList_layout()

    def loginPage(self):
        verify = 0
        # Creating window for login
        # Creating size, title for window
        self.loginWindow = Toplevel(self.mainwin)
        self.loginWindow.wm_title("Login")
        self.loginWindow.geometry("300x155")
        self.loginWindow.resizable(width=0, height=0)
        self.loginWindow.attributes('-topmost', 'true')
        self.mainwin.eval(f'tk::PlaceWindow {str(self.loginWindow)} center')
        self.loginWindow.grab_set()
        self.loginWindow.iconbitmap("Logo_DraftAAT.ico")
        # Creating frame for widgets
        loginFrame = Frame(self.loginWindow)
        emailFrame = Frame(self.loginWindow, width=30)
        passwrdFrame = Frame(self.loginWindow, width=30)

        # Creating widget objects
        loginBtn = Button(loginFrame, text="Login", font=('Helvetica', 10))

        emailLabel = Label(emailFrame, text="Email: ", font=('Helvetica', 10), padx=55)
        passwrdLabel = Label(passwrdFrame, text="Password: ", font=('Helvetica', 10), padx=55)
        wrongPassLabel = Label(loginFrame, text="No matching credentials, please try again", font=('Helvetica', 10))

        self.emailEntry = Entry(emailFrame, width=30)
        self.passwrdEntry = Entry(passwrdFrame, width=30)

        # Placing widgets on the screen
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

        # Using the rest API to verify credentials
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


    # Creates the widgets for the fouryear plan
    def FourYearPlan(self):
        # ============================ Scroll Bar ============================
        self.canvas = Canvas(self.leftFrame, width=self.left_width)  # Creating Canvas for scrollbar
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.scrollbar = Scrollbar(self.leftFrame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.innerLeftFrame = Frame(self.canvas)
        self.innerLeftFrame.pack(expand=1)

        self.canvas.create_window((0, 0), window=self.innerLeftFrame, anchor=NW, width=self.left_width)

        # ============================ title ============================
        FYPTitleFrame = Frame(self.innerLeftFrame, width=self.left_width, height=50)
        FYPTitleFrame.pack(pady=20)

        FYPTitle = Label(FYPTitleFrame, text="Academic Advising", anchor=CENTER,
                             font=('Helvetica', 19))
        FYPTitle.pack(side=TOP)

        # ============================ Student Name and ID ============================

        nameIDFrame = Frame(self.innerLeftFrame, width=self.left_width, height=50)
        nameIDFrame.pack(ipadx=30, ipady=10)

        nameLabel = Label(nameIDFrame, text='Name:')
        nameLabel.pack(side=LEFT, expand=1)

        self.FYPnameEntry = Entry(nameIDFrame)
        self.FYPnameEntry.pack(side=LEFT, expand=1)

        self.id2Entry = Entry(nameIDFrame, width=8)
        self.id2Entry.pack(side=RIGHT, expand=1)

        idLabel = Label(nameIDFrame, text='ID Number:')
        idLabel.pack(side=RIGHT, expand=1)

        # ============================ Progress Report ============================
        # Creation of Notebook to add tabs to Academic Advising screen
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

        # Adds the progress report tab Notebook
        self.tab_parent.add(self.progressRepoFrame, text="Progress Report")

        # Creating buttons for Progress Report placing with .grid() in FYP_addCourseButton
        self.addProgRepoBtn = Button(self.progressRepoFrame, text="Add Course", command=lambda: self.FYP_addCourseButton())
        self.removeProgRepoBtn = Button(self.progressRepoFrame, text="Remove Course", command=lambda: self.FYP_delCourseButton(self.mainwin))

        # ============================ Add Semester Table Button ============================

        self.addSemesterBtn = Button(self.progressRepoFrame, text="Add Semester")
        self.addSemesterBtn['command'] = lambda:  self.addSemester(self.progressRepoFrame, self.progLabel, self.progTable)

        self.removeSemesterBtn = Button(self.progressRepoFrame, text="Remove Semester")
        self.removeSemesterBtn['command'] = lambda: self.removeSemester(self.progressRepoFrame, self.progLabel,
                                                                  self.progTable)

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

        self.coursesNeeded = []

        self.minorReqList = minorReqList  # Copying minor requirements to use as labels for creatTable()
        self.policies = policies  # Copying policies for other functions
        self.courseHist = courseHist
        self.progTableLength = len(courseHist)  # Storing the amount of semesters to make that many treeviews in createTable
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
        self.createTable(self.progressRepoFrame, self.progLabel, self.progTable, self.progTableLength + 1)

        # Filling winter and summer courses
        self.winSumTable = []
        self.winSumLabel = []

        self.createWinSumTable(self.progressRepoFrame, self.winSumLabel, self.winSumTable, self.progTableLength + 2)

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
            self.tab_parent.add(self.majorFrames[i], text=major[i])  # Each frame to the Notebook to display tab
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
            self.tab_parent.add(self.minorFrames[i], text=minor[i])  # Each frame to the Notebook to display tab
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
                    self.coursesNeeded.append(str(course[1] + " " + course[2]))
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
                    self.coursesNeeded.append(str(course[1] + " " + course[2]))
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
            self.tab_parent.add(self.majorFrames[i], text=major[i])  # Each frame to the Notebook to display tab

        for i in range(len(minor)):  # Filling arrays according to amount of majors a student is doing
            self.sizeOfMinor = len(self.minorReqList[i])  # Amount of tables and labels for each minor
            self.minorsLabelArray.append([])  # Creates 2d array for each each array containing labels for a tab
            self.minorsTable.append([])  # Creates 2d array each array is a minor containing each treeview for a tab
            self.minorFrames.append(Frame(self.tab_parent))  # Holds frames for each tab
            self.createMinorTable(self.minorFrames[i], self.minorsLabelArray[i],
                                  self.minorsTable[i])  # Function to populate these arrays
            self.tab_parent.add(self.minorFrames[i], text=minor[i])  # Each frame to the Notebook to display tab

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

        self.addSemesterBtn.forget()
        self.removeSemesterBtn.forget()

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

        self.FYPnameEntry.delete(0, END)
        self.id2Entry.delete(0, END)
        self.FYPnameEntry.config(state=NORMAL)
        self.id2Entry.config(state=NORMAL)

        self.addSemesterBtn.grid_remove()
        self.removeSemesterBtn.grid_remove()

        while (self.tab_parent.index("end") != 1):  # Removes the tabs but leaves Progress Report tab
            self.tab_parent.forget(self.tab_parent.index("end") - 1)

    # Called when deleting a course using delete course button in FYP
    def FYP_delCourseButton(self, parentWindow):
        msg = "Do you want to remove the selected course? ("
        cnt = 0
        index = {}
        tbl = ""
        maxRng = 0
        tbl = self.progTable
        maxRng = len(self.progTable)

        # Loops thru each of selected tree view values and pushes the index into a list
        for i in range(0, maxRng):
            for course in tbl[i].selection():
                index[cnt] = [i, course]
                cnt += 1
        # If only one course selected
        if len(index) == 1:
            msg = "Do you want to remove the selected course? (" + tbl[index[0][0]].item(index[0][1])['values'][0] + ")"
        # Else create msg prompt for batch delete courses
        else:
            msg = "Do you want to remove the selected course? ("
            for i in range(len(index)):
                msg = msg + tbl[index[i][0]].item(index[i][1])['values'][0]
                if i + 1 != len(index):
                    msg += ", "
            msg = msg + ")"
        # If answer yes then proceed with course deletion
        response = messagebox.askquestion("askquestion", msg)
        for i in range(len(index)):
            self.tot_Removed += 1
            if response == 'yes':
                tbl[index[i][0]].delete(index[i][1])
                if type == 1:
                    self.progTableTree_iid -= 1
                else:
                    self.progTableTree_iid -= 1

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
                ttk.Treeview(frame, height=7, style="mystyle.Treeview", takefocus=True, selectmode="extended"))

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

            if i < math.ceil(length / 2):
                labels.append(Label(frame, text="Year " + str(i + 1), font=('Helvetica', 15)))

        # grid labels
        for i in range(math.ceil(length / 2)):
            labels[i].grid(column=0, row=2 * i, columnspan=2, sticky=W, padx=5)

        # grid treeviews
        if length % 2 == 0:
            for i in range(0, length, 2):
                tables[i].grid(column=0, row=i + 1)
                tables[i + 1].grid(column=1, row=i + 1)
        else:
            for i in range(0, length, 2):
                if i == length-1:
                    tables[i].grid(column=0, row=i + 1)
                else:
                    tables[i].grid(column=0, row=i + 1)
                    tables[i + 1].grid(column=1, row=i + 1)

    def removeSemester(self, frame, labels, tables):
        # column configure
        for i in range(2):
            frame.columnconfigure(i, weight=1)

        # define treeviews and labels
        tables[len(tables) - 1].forget()
        tables[len(tables) - 1].grid_remove()
        tables.pop()

        self.prevProgTableLength = len(self.progTable) - 1

        # Identifies if the progress reports has an even or odd number of semesters
        # Then adds the the label, table, and add semester button to correct locations
        if self.prevProgTableLength % 2 == 0:
            self.addSemesterBtn.grid(row=self.prevProgTableLength - 2, column=1)
            self.removeSemesterBtn.grid(row=self.prevProgTableLength - 2, column=1)
            labels[len(labels) - 1].forget()
            labels[len(labels) - 1].grid_remove()
            labels.pop()

            self.winSumLabel[0].grid(column=0, row=self.prevProgTableLength - 4)
            self.winSumTable[0].grid(column=0, row=self.prevProgTableLength - 5, columnspan=2, sticky=W, padx=5)
            self.winSumLabel[1].grid(column=1, row=self.prevProgTableLength - 4)
            self.winSumTable[1].grid(column=1, row=self.prevProgTableLength - 5, columnspan=2, sticky=W, padx=5)

        else:
            self.addSemesterBtn.grid(row=self.prevProgTableLength + 1, column=0)
            self.removeSemesterBtn.grid(row=self.prevProgTableLength + 1, column=0)

        self.canvas.update()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.progTableLength -= 1
    # Creates a table of treeviews for progress report tab
    def addSemester(self, frame, labels, tables):

        # column configure
        for i in range(2):
            frame.columnconfigure(i, weight=1)
        # define treeviews and labels
        tables.append(
            ttk.Treeview(frame, height=7, style="mystyle.Treeview", takefocus=True, selectmode="none"))

        self.prevProgTableLength = len(self.progTable) - 1

        tables[len(tables)-1]['columns'] = ("course#", "title", "cred")
        tables[len(tables)-1].column("#0", width=0, stretch=NO)
        tables[len(tables)-1].column("course#", anchor=CENTER, width=90)
        w = int((self.left_width - 300) / 2)
        tables[len(tables)-1].column("title", anchor=W, width=w)
        tables[len(tables)-1].column("cred", anchor=CENTER, width=35)

        tables[len(tables)-1].heading("course#", text='Course #', anchor=CENTER)
        tables[len(tables)-1].heading("title", text='Title', anchor=CENTER)
        tables[len(tables)-1].heading("cred", text='CR', anchor=CENTER)

        # Identifies if the progress reports has an even or odd number of semesters
        # Then adds the the label, table, and add semester button to correct locations
        if self.prevProgTableLength % 2 == 0:
            tables[len(tables) - 1].grid(column=0, row=self.prevProgTableLength + 1)
            self.addSemesterBtn.grid(row=self.prevProgTableLength + 1, column=1)

        else:
            tables[len(tables) - 1].grid(column=1, row=self.prevProgTableLength)
            labels.append(
                Label(frame, text="Year " + str(math.ceil(self.prevProgTableLength / 2) + 1), font=('Helvetica', 15)))
            labels[len(labels) - 1].grid(column=0, row=self.prevProgTableLength + 1, columnspan=2, sticky=W, padx=5)
            self.addSemesterBtn.grid(row=self.prevProgTableLength + 2, column=0)

            self.winSumLabel[0].grid(column=0, row=self.prevProgTableLength + 4)
            self.winSumTable[0].grid(column=0, row=self.prevProgTableLength + 5, columnspan=2, sticky=W, padx=5)
            self.winSumLabel[1].grid(column=1, row=self.prevProgTableLength + 4)
            self.winSumTable[1].grid(column=1, row=self.prevProgTableLength + 5, columnspan=2, sticky=W, padx=5)

        self.canvas.update()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.progTableLength += 1

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

            tables[i].heading("course#", text='Course #', anchor=CENTER)
            tables[i].heading("title", text='Title', anchor=CENTER)
            tables[i].heading("cred", text='CR', anchor=CENTER)

            if i < len(tables):
                labels.append(Label(frame, font=('Helvetica', 12)))

            # grid labels
            row = 0
            if len(tables) == 1:
                tables[i].grid(column=0, row=row + 2)
                labels[i].grid(column=0, row=row + 1, columnspan=1, sticky=W, padx=150)
            else:
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

            tables[i].heading("course#", text='Course #', anchor=CENTER)
            tables[i].heading("title", text='Title', anchor=CENTER)
            tables[i].heading("cred", text='CR', anchor=CENTER)

        labels.append(Label(frame, text="Winter Courses", font=('Helvetica', 15)))
        labels.append(Label(frame, text="Summer Courses", font=('Helvetica', 15)))

        labels[0].grid(column=0, row=length + 2, columnspan=2, sticky=W, padx=5)
        tables[0].grid(column=0, row=length + 3)

        labels[1].grid(column=1, row=length + 2, columnspan=2, sticky=W, padx=5)
        tables[1].grid(column=1, row=length + 3)

    # Called when there is a course added to a treeview in FYP
    def FYP_addCourseButton(self):
        t = Toplevel(self.mainwin)
        t.wm_title("Search for Course")
        t.geometry("700x500")
        t.resizable(width=FALSE, height=FALSE)
        t.transient(self.mainwin)
        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')
        self.selectedSemester = ''
        self.addSemesterBtn["state"] = DISABLED

        # Closes window
        def close(e):
            self.addCourseButton.configure(state=NORMAL)
            self.addSemesterBtn["state"] = NORMAL
            t.destroy()

        t.bind('<Destroy>', close)
        self.addCourseButton.configure(state=DISABLED)

        # Updates list on course tree
        def update_course_list(data):
            for i in self.course_tree.get_children():
                self.course_tree.delete(i)

            for item in data:
                self.course_tree.insert('', 'end',
                                   values=(item['Subject'], item['Catalog'], item['Long Title'], item['Allowd Unt']))
        # Fills out entries
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
        # Verifying course exits
        def check_course(event):
            subject_type = subject_entry.get().upper()
            catalog_type = catalog_entry.get()
            title_type = title_entry.get().upper()
            credit_type = credit_entry.get()

            pub.sendMessage("request_Course_by_Regex", sub=subject_type, cat=catalog_type, title=title_type, cred=credit_type)
            update_course_list(self.course_regex_list)

        # adds searched course into the treeview
        def addCourse():
            self.courseTree_counter += 1
            subject_type = subject_entry.get().upper()
            catalog_type = catalog_entry.get()
            title_type = title_entry.get().upper()
            credit_type = credit_entry.get()
            self.selectedSemester.insert(parent='', index='end', iid=self.courseTree_counter, text="",
                                   values=(subject_type + " " + catalog_type,
                                           title_type,
                                           credit_type,
                                           "Major"))

            prevcred = self.enrollCredVar.get()
            self.enrollCredVar.set(prevcred + int(float(credit_type)))

        self.dropDefault = StringVar()
        self.dropDefault.set("Select a semester")
        self.semesters = []

        print(len(self.courseHist))
        print(self.progTableLength)
        for i in range(0, len(self.courseHist), 1):
            if i % 2 == 0:
                self.semesters.append("Year " + str(math.ceil(i/2)+1) + " Semester " + str(1))
            elif i == len(self.courseHist):
                self.semesters.append("Current Semester ")
            else:
                self.semesters.append("Year " + str(math.ceil(i/2)) + " Semester " + str(2))
        self.semesters.append('Winter')
        self.semesters.append('Summer')

        # Changed the semester on dropdown
        def semesterChanged(event):
            comboboxString = self.progRepoDrop.get().split()
            if comboboxString[0] == 'Winter':
                self.selectedSemester = self.winSumTable[0]
            elif comboboxString[0] == 'Summer':
                self.selectedSemester = self.winSumTable[1]
            elif comboboxString[3] == '1':
                self.selectedSemester = self.progTable[(int(comboboxString[1]))*2 - 2]
            else:
                self.selectedSemester = self.progTable[(int(comboboxString[1]))*2 - 1]

        self.subject_frame = Frame(t, borderwidth=2)
        self.subject_frame.pack(side=LEFT, anchor='n', padx=10)
        selectedSemester = ''
        self.progRepoDrop = ttk.Combobox(self.subject_frame, value=self.semesters, exportselection=0, width=18)
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

    # Creates widgets for left side of program
    def planningWorksheet_layout(self):
        self.rightFrame = Frame(self.PPWFrame)
        self.rightFrame.pack(fill=BOTH)

        for i in range(4):
            self.rightFrame.columnconfigure(i, weight=1)

        pad = 10  # pady value for most frames below

        # ============================ title ============================
        ProgPlanTitle = Label(self.rightFrame, text="Program Planning Worksheet", anchor=CENTER,
                                  font=('Helvetica', 19))
        ProgPlanTitle.grid(row=0, column=0, columnspan=4, pady=20)

        # ============================ student name ============================
        nameFrame = Frame(self.rightFrame)
        nameFrame.grid(row=2, column=0, columnspan=2, pady=pad)

        nameLabel = Label(nameFrame, text='Name:')
        nameLabel.pack(side=LEFT)

        self.nameEntry = Entry(nameFrame)
        self.nameEntry.pack()

        # ============================ student id ============================
        idFrame = Frame(self.rightFrame)
        idFrame.grid(row=2, column=2, columnspan=2, pady=pad)

        idLabel = Label(idFrame, text='ID Number:')
        idLabel.pack(side=LEFT)

        self.idEntry = Entry(idFrame, width=8, justify=CENTER)
        self.idEntry.pack()

        # ============================ season ============================
        seasonFrame = Frame(self.rightFrame)
        seasonFrame.grid(row=4, column=0, columnspan=4, pady=pad)

        self.seasonVar = StringVar()

        seasonLabel = Label(seasonFrame, text='Registering for:')
        fallRadioBtn = Radiobutton(seasonFrame, text='Fall', variable=self.seasonVar, value='Fall')
        summerRadioBtn = Radiobutton(seasonFrame, text='Summer', variable=self.seasonVar, value='Summer')
        springRadioBtn = Radiobutton(seasonFrame, text='Spring', variable=self.seasonVar, value='Spring')
        winterRadioBtn = Radiobutton(seasonFrame, text='Winter', variable=self.seasonVar, value='Winter')

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

        self.editCareerButton = Button(careerFrame, text="Add/Remove", command=self.editMajorMinor)
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
        self.earnCredEntry = Entry(credFrameL, width=3, justify=CENTER, state=DISABLED)
        credLabel2 = Label(credFrameL, text='credits.')

        credLabel1.grid(row=0, column=0)
        self.earnCredEntry.grid(row=0, column=1)
        credLabel2.grid(row=0, column=2)

        credLabel3 = Label(credFrameR, text='Currently Enrolled in.')
        self.enrollCredVar = IntVar()
        self.enrollCredEntry = Entry(credFrameR, width=3, textvariable=self.enrollCredVar, justify=CENTER)
        credLabel4 = Label(credFrameR, text='Credits')

        credLabel4.grid(row=0, column=0)
        self.enrollCredEntry.grid(row=0, column=1)
        credLabel3.grid(row=0, column=2)

        # ====================== Enrollment Date ========================
        enrlDateFrame = Frame(self.rightFrame)
        enrlDateFrame.grid(row=10, column=0, columnspan=4, pady=pad)

        enrlDate = Label(enrlDateFrame, text='Enrollment Date:')
        enrlDate.pack(side=LEFT)

        self.enrlDateEntry = Entry(enrlDateFrame, width=8, justify=CENTER)
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
        memoFrame = LabelFrame(self.rightFrame, text='Memo:')
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

        self.addCourseButton = Button(coursebuttonFrame, text="Add", command=self.planningWorksheet_addCourseButton)
        self.addCourseButton.pack(side=LEFT)

        rmCourseButton = Button(coursebuttonFrame, text="Remove", command=self.planningWorksheet_delCourseButton)
        rmCourseButton.pack(side=RIGHT)

        # backup course
        bcoursebuttonFrame = Frame(self.rightFrame)
        bcoursebuttonFrame.grid(row=15, column=0, columnspan=4)

        self.addBackupButton = Button(bcoursebuttonFrame, text="Add",
                                          command=self.planningWorksheet_addBackupCourseButton)
        self.addBackupButton.pack(side=LEFT)

        rmBackupButton = Button(bcoursebuttonFrame, text="Remove",
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

        # Closes the window
        def close(e):
            self.editCareerButton.configure(state=NORMAL)

        t.bind('<Destroy>', close)
        self.editCareerButton.configure(state=DISABLED)

        # insert selected major into separate listbox
        def majorSelection(e):
            maj = self.majorBox.curselection()
            maj_txt = self.majorBox.get(maj)
            inTree = FALSE
            for i, entry in enumerate(self.selected_major_Box.get(0, END)):
                if str(maj_txt) == entry:
                    inTree = TRUE
                    messagebox.showwarning(parent=t, title="Duplicate Major Error", message="Error: Unable to Add Duplicate Major to Table")
            if not inTree:
                self.selected_major_Box.insert(END, self.majorBox.get(maj))
        # Removes a major
        def removeMajor():
            try:
                i = self.selected_major_Box.curselection()
                msg = "Do you want to remove selected major? (" + self.selected_major_Box.get(i) + ")"
                response = messagebox.askquestion("askquestion", msg, parent=t)
                if response == 'yes':
                    self.selected_major_Box.delete(i)
                    majorRemoveButton["state"] = DISABLED
                    # self.selected_major_Box.bind('<FocusOut>', lambda e: self.selected_major_Box.selection_clear(0, END))
            except(TclError):
                messagebox.showwarning(parent=t, title="Invalid Selection", message="Error: Unable to Remove, No Minor Selected")

        # insert selected minor into separate listbox
        def minorSelection(e):
            min = self.minorBox.curselection()
            min_txt = self.minorBox.get(min)
            inTree = FALSE
            for i, entry in enumerate(self.selected_minor_Box.get(0, END)):
                if str(min_txt) == entry:
                    inTree = TRUE
                    messagebox.showwarning(parent=t, title="Duplicate Major Error", message="Error: Unable to Add Duplicate Minor to Table")
            if not inTree:
                self.selected_minor_Box.insert(END, self.minorBox.get(min))

        # Removes a minor
        def removeMinor():
            try:
                i = self.selected_minor_Box.curselection()
                msg = "Do you want to remove selected minor? (" + self.selected_minor_Box.get(i) + ")"
                response = messagebox.askquestion("askquestion", msg, parent=t)
                if response == 'yes':
                    self.selected_minor_Box.delete(i)
                    minorRemoveButton["state"] = DISABLED
            except(TclError):
                messagebox.showwarning(parent=t, title="Invalid Selection", message="Error: Unable to Remove, No Minor Selected")

        # Confirms selection of treeview
        def confirmSelection():
            self.setMajor_treeview()
            self.setMinor_treeview()
            self.editCareerButton.configure(state=NORMAL)
            # clear tabs from left side
            while (self.tab_parent.index("end") != 1):
                self.tab_parent.forget(self.tab_parent.index("end") - 1)
            self.FYP_refresh()
            t.destroy()

        # Enables user to click button
        def enableMajorRemoveBtn(e):
            majorRemoveButton["state"] = "NORMAL"

        # Enables user to click button
        def enableMinorRemoveBtn(e):
            minorRemoveButton["state"] = "NORMAL"

        mainframe = Frame(t)
        mainframe.pack(fill=X, ipadx=1, padx=10)

        majorframe = LabelFrame(mainframe, text="Current Major(s)")
        majorframe.pack(side=LEFT, pady=5)

        minorframe = LabelFrame(mainframe, text="Current Minor(s)")
        minorframe.pack(side=RIGHT, pady=5)

        self.selected_major_Box = Listbox(majorframe, selectmode=SINGLE, justify=CENTER, exportselection=False,
                                          height=4)
        self.selected_major_Box.pack(side=TOP)
        self.selected_major_Box.bind("<<ListboxSelect>>", enableMajorRemoveBtn)

        self.selected_minor_Box = Listbox(minorframe, selectmode=SINGLE, justify=CENTER, exportselection=False,
                                          height=4)
        self.selected_minor_Box.pack(side=TOP)
        self.selected_minor_Box.bind("<<ListboxSelect>>", enableMinorRemoveBtn)

        majorRemoveButton = Button(majorframe, text="Remove", command=removeMajor, state=DISABLED)
        majorRemoveButton.pack()

        minorRemoveButton = Button(minorframe, text="Remove", command=removeMinor, state=DISABLED)
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

        comfirmButton = Button(t, text="Save", command=confirmSelection)
        comfirmButton.pack(side=BOTTOM, pady=10)

    # end goal: return array of major under specified school
    def getMajorBySchool(self, e):
        pub.sendMessage("request_major", sch=self.schCbox1.get())

    # end goal: return array of minor under specified school
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

    # Makes sure FYP has correct values
    def FYP_refresh(self):
        majors, minors = [], []
        for id in self.majorTree.get_children():
            majors.append(self.majorTree.item(id)['text'])
        for id in self.minorTree.get_children():
            minors.append(self.minorTree.item(id)['text'])
        pub.sendMessage("refresh_fyp", majors=majors, minors=minors)

    # Setting values of treeview
    def setMinor_treeview(self):
        for id in self.minorTree.get_children():
            self.minorTree.delete(id)

        self.selected_minor_Box.select_set(0, END)
        for i in self.selected_minor_Box.curselection():
            word = self.selected_minor_Box.get(i)
            self.minorTree.insert(parent='', index='end', iid=i, text=str(word))

    # Adding a course on planning worksheet side
    def planningWorksheet_addCourseButton(self):
        t = Toplevel(self.mainwin)
        t.wm_title("Search for Course")
        t.geometry("700x400")
        t.resizable(width=FALSE, height=FALSE)
        t.transient(self.mainwin)
        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')

        # Closes window
        def close(e):
            self.addCourseButton.configure(state=NORMAL)
            t.destroy()

        t.bind('<Destroy>', close)
        self.addCourseButton.configure(state=DISABLED)

        # Update course list for treeview
        def update_course_list(data):
            for i in self.course_tree.get_children():
                self.course_tree.delete(i)

            #self.course_tree.tag_configure('evenrow', background="grey")
            #self.course_tree.tag_configure('oddrow', background="white")

            for item in data:
                self.course_tree.insert('', 'end',
                                   values=(item['Subject'], item['Catalog'], item['Long Title'], item['Allowd Unt']))

        # Fills out fields for entries
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
        # Checks if course is available
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

            if subject_type == "" or catalog_type == "" or title_type == "":
                messagebox.showwarning(parent=t, title="Invalid Input", message="Error: No Fields Can Be Left Blank")
            else:
                inTree = FALSE
                tree_values = self.courseTree.get_children()
                for each in tree_values:
                    if title_type == self.courseTree.item(each)['values'][1]:
                        inTree = TRUE
                        messagebox.showwarning(parent=t, title="Duplicate Course Error", message="Error: Unable to add duplicate course to table")

                if not inTree:
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

    # Used when deleting a course
    def planningWorksheet_delCourseButton(self):
        for course in self.courseTree.selection():
            msg = "Do you want to remove the selected course? (" + self.courseTree.item(course)['values'][0] + ")"
            response = messagebox.askquestion("askquestion", msg)
            if response == 'yes':
                prevcred = self.enrollCredVar.get()
                self.enrollCredVar.set(prevcred - int(float(self.courseTree.item(course)['values'][2])))

                self.courseTree.delete(course)
                self.courseTree_counter -= 1

    # Adds a course to the backup course treeview
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

        # Updates backup course list
        def backup_update_course_list(data):
            for i in self.backup_addCourseTree.get_children():
                self.backup_addCourseTree.delete(i)

            # self.course_tree.tag_configure('evenrow', background="grey")
            # self.course_tree.tag_configure('oddrow', background="white")

            for item in data:
                self.backup_addCourseTree.insert('', 'end',
                                        values=(
                                        item['Subject'], item['Catalog'], item['Long Title'], item['Allowd Unt']))

        # Fills out entries
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

        # Checks if course is available
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

            if subject_type == "" or catalog_type == "" or title_type == "":
                messagebox.showwarning(parent=t, title="Invalid Input", message="Error: No Fields Can Be Left Blank")
            else:
                inTree = FALSE
                tree_values = self.backupCourseTree.get_children()
                for each in tree_values:
                    if title_type == self.backupCourseTree.item(each)['values'][1]:
                        inTree = TRUE
                        messagebox.showwarning(parent=t, title="Duplicate Course Error", message="Error: Unable to add duplicate course to table")
                if not inTree:
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

    # Deletes course from the backup course treeview
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

    # Fills PPW with information
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
    #     memoFrame = LabelFrame(self.pop, text='Memo:')
    #     memoFrame.grid(row=16, column=0, columnspan=4, pady=10)
    #
    #     self.memoEntry = Text(memoFrame, width=60, height=7)
    #     self.memoEntry.pack()
    #
    #     self.memoEntry.delete('1.0', 'end')
    #     self.memoEntry.insert('1.0', self.memo_to_display)

    # Creates University policy box
    def univ_policy_box(self):
        self.pop = Toplevel(self.innerLeftFrame)
        self.pop.title("University Policies")
        self.pop.geometry("720x360")
        self.pop.config(bg="white")

        # ============================ Policy Memo ============================
        policyFrame = LabelFrame(self.pop, height=200, width=self.left_width,
                                     text='University Policy:')
        policyFrame.pack(pady=30)

        self.policyMemoEntry = Text(policyFrame, width=90, height=10)
        self.policyMemoEntry.pack()

        self.policyMemoEntry.config(state=NORMAL)
        self.policyMemoEntry.delete('1.0', 'end')
        self.policyMemoEntry.insert('1.0', self.policy_to_display)
        self.policyMemoEntry.config(state=DISABLED)

    # Course taken layout for treeview
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
    # Course taken list restting values
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
    # Creating menu bar
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

    # Help page for application
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

    # Function for when new schudule is clicked in menu
    def newSchedule(self):
        self.planningWorksheet_reset()
        self.FYP_reset()
        self.courseTakenList_reset()
        # Removes buttons when student information is not present
        self.addProgRepoBtn.grid_forget()
        self.removeProgRepoBtn.grid_forget()

    # Called when clicked in the menu to bring up open schudule window
    def openSchedule(self):
        pub.sendMessage("requestStudents")

        t = Toplevel(self.mainwin)
        t.wm_title("Search for Student")
        t.geometry("440x350")
        t.resizable(width=0, height=0)
        t.attributes('-topmost', 'true')
        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')

        # Searches for the students name to open their schudule
        def openScheduleSearchButton(e):
            if fname.get() == "" or lname.get() == "" or idE.get() == "":
                w = Toplevel(t)
                w.wm_title("Invalid Input")
                w.geometry("330x120")

                w.grab_set()
                top = Frame(w, bg='White')
                top.pack(side="top", expand=TRUE, fill=BOTH)

                msg = Label(top, text="Error: Search Fields Cannot Be Blank", bg="White", font=('Helvetica', 9))
                msg.pack(anchor='n', pady=20)
                bottom = Frame(w)
                bottom.pack(side="bottom", fill=Y, anchor='e', ipady=10)
                btn = Button(bottom, text="OK", relief=GROOVE, font=('Helvetica', 9), command=lambda: w.destroy())
                btn.pack(side=RIGHT, ipadx=20, padx=15)
            else:
                try:
                    self.studentBox.curselection()
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
                        self.addProgRepoBtn.grid(column=0, row=0, sticky=E, padx=150)
                        self.removeProgRepoBtn.grid(column=0, row=0, sticky=E, padx=10)
                        self.progLabel[len(self.progLabel) - 1]['text'] = 'Current Semester'
                        if self.progTableLength % 2 == 0:
                            self.addSemesterBtn.grid(row=self.progTableLength + 1, column=1)
                        else:
                            self.addSemesterBtn.grid(row=self.progTableLength + 2, column=0)
                            self.progLabel.append(Label(self.progressRepoFrame,
                                                        text="Year " + str(math.ceil(self.progTableLength / 2) + 1),
                                                        font=('Helvetica', 15)))
                            self.progLabel[len(self.progLabel) - 1].grid(column=0, row=self.progTableLength + 1,
                                                                         columnspan=2, sticky=W, padx=5)


                except (TclError):
                    w = Toplevel(t)
                    w.wm_title("Invalid Input")
                    w.geometry("330x120")
                    w.resizable(width=0, height=0)
                    w.attributes('-topmost', 'true')
                    self.mainwin.eval(f'tk::PlaceWindow {str(w)} center')
                    w.grab_set()
                    top = Frame(w, bg='White')
                    top.pack(side="top", expand=TRUE, fill=BOTH)

                    msg = Label(top, text="Error: Result Not Found, Check Search Fields are Correct", bg="White",
                                font=('Helvetica', 9))
                    msg.pack(anchor='n', pady=20)
                    bottom = Frame(w)
                    bottom.pack(side="bottom", fill=Y, anchor='e', ipady=10)
                    btn = Button(bottom, text="OK", relief=GROOVE, font=('Helvetica', 9), command=lambda: w.destroy())
                    btn.pack(side=RIGHT, ipadx=20, padx=15)

        # Filters the students out when typing in entry feilds
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
        # Automatically fills entry when clicking on student in student box
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

        # Closes window
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
        fname = Entry(nameFrame, width=10)
        fname.pack(side=LEFT)
        fname.bind("<KeyRelease>", filtr)

        lname = Entry(nameFrame, width=15)
        lname.pack(side=RIGHT)
        label3 = Label(nameFrame, text='Last name:').pack(side=RIGHT)
        lname.bind("<KeyRelease>", filtr)

        label3 = Label(idFrame, text='Student Id:').pack(side=LEFT)
        idE = Entry(idFrame, width=10)
        idE.pack(side=LEFT)
        idE.bind("<KeyRelease>", filtr)

        searchB = Button(butFrame, text='Open')
        searchB.pack()
        searchB.bind("<ButtonRelease>", openScheduleSearchButton)

        mainframe = Frame(t)
        mainframe.pack(fill=X, ipadx=1, padx=100, pady=10)

        studentFrame = LabelFrame(mainframe, text="Students")
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

    # To save the information in the widgets to the database
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

    # Calls the export function for making a PDF
    def exportSchedule(self):
        fnameE = "{}.pdf".format(self.nameEntry.get())
        pub.sendMessage("export_schedule", id=self.idEntry.get(), fname=fnameE)

    # Prints the schedule of PDF
    def printSchedule(self):
        print("Print schedule")

    # Loads the menu
    def loadMenu(self, major):
        major.add_command(label='Four Year Plan', command=self.showFourYearPlan)
        major.add_command(label='Course Taken List', command=self.showCourseTakenList)

    # Switching from coursetaken list to PPW and progress report
    def showFourYearPlan(self):
        self.courseTakenListFrame.pack_forget()
        self.PPWFrame.pack_forget()
        self.leftFrame.pack(side=LEFT, fill=Y, padx=5)
        self.PPWFrame.pack(side=RIGHT, fill=Y)
        self.PPWFrame.pack_propagate(0)

    # Shows Course taken list
    def showCourseTakenList(self):
        self.leftFrame.pack_forget()
        self.courseTakenListFrame.pack(side=LEFT, fill=Y, padx=5)
        self.courseTakenListFrame['width'] = self.left_width
        self.courseTakenListFrame.propagate(0)

    # OpensCSV calling the function from the model
    def openCSV(self):
        pub.sendMessage("request_CSV")

    # Closes the window
    def close(self, window):
        window.destroy()

    # PPW edit major add course button to add course to treeview in edit major window
    def planningWorksheet_editMajor_addCourseButton(self, parentWindow, type):
        t = Toplevel(parentWindow)
        t.wm_title("Search for Course")
        t.geometry("700x500")
        t.resizable(width=FALSE, height=FALSE)
        t.transient(self.mainwin)
        t.attributes('-topmost', 'true')
        selectedTreeView = self.mainwin.focus_get()
        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')

        tbl = ""
        maxRng = 0
        if type == 1:
            tbl = self.edtMiTbls
            maxRng = len(self.minorsFYP)
        else:
            tbl = self.edtMjTbls
            maxRng = len(self.majorsFYP)

        # Closes window
        def close(e):
            self.addCourseButton.configure(state=NORMAL)
            t.destroy()

        t.bind('<Destroy>', close)
        self.addCourseButton.configure(state=DISABLED)

        # Updates the courses for treeview
        def update_course_list(data):
            for i in self.course_tree.get_children():
                self.course_tree.delete(i)

            #self.course_tree.tag_configure('evenrow', background="grey")
            #self.course_tree.tag_configure('oddrow', background="white")

            for item in data:
                self.course_tree.insert('', 'end',
                                   values=(item['Subject'], item['Catalog'], item['Long Title'], item['Allowd Unt']))

        # Fills out entries for fields
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
        # Check if course is available to get
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
            ind = self.clicked.get()
            int_ind = int(ind) - 1
            blank = False
            blank_ind = 0
            if subject_type == "" or catalog_type == "" or title_type == "":
                messagebox.showwarning(parent=t, title="Invalid Input", message="Error: No Fields Can Be Left Blank")
            else:
                inTree = False
                for i in range(0, maxRng):
                    cnt = len(tbl[i].get_children())
                    for num in range(cnt):
                        try:    # Checks if a course was previously removed from a table before proceeding
                            tbl[i].item(num)
                            if title_type == tbl[i].item(num)['values'][1] or subject_type + catalog_type == tbl[i].item(num)['values'][0]:
                                inTree = True
                                messagebox.showinfo(parent=t, title="Duplicate Course Error",
                                                    message="Error: Course Already Exists in Plan")
                        except TclError as err: # If a course has been removed and causes a index error
                            if i == int_ind:    # If that index error occurs in the same treeview that user attempts to insert
                                blank = True    # Indicate there is a blank
                                blank_ind = num # Store the index to be used in insertion
                if not inTree:
                    if blank == True:       # If theres a blank
                        cnt = blank_ind     # Use the blank index as the IID
                    else:                   # Else use the end IID
                        cnt = len(tbl[int_ind].get_children())
                    tbl[int_ind].insert(parent='', index='end', iid=cnt,
                                                   values=(
                                                       (subject_type + " " + catalog_type), title_type, credit_type))
                    if type == 1:
                        self.edtMiTbls_iid += 1
                    else:
                        self.edtMjTbls_iid += 1


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

        self.semester_frame = Label(self.subject_frame, text="Choose the Semester to add Course",
                                  font=("Helvetica", 10), fg="black")
        self.semester_frame.pack(pady=5, anchor='n')

        self.clicked = StringVar()
        options = [1, 2, 3, 4, 5, 6, 7, 8]
        drop = OptionMenu(self.subject_frame, self.clicked, *options)
        drop.pack(pady=5, anchor='n')

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

    # Delete course button for edit major to delete a course in that window
    def openMajor_editMajor_delCourseButton(self, type):
        msg = "Do you want to remove the selected backup course? ("
        cnt = 0
        index = {}
        tbl = ""
        maxRng = 0
        if type == 1:
            tbl = self.edtMiTbls
            maxRng = len(self.minorsFYP)
        else:
            tbl = self.edtMjTbls
            maxRng = len(self.majorsFYP)
        # Loops thru each of selected tree view values and pushes the index into a list
        for i in range(0, maxRng):
            for course in tbl[i].selection():
                index[cnt] = [i, course]
                cnt+=1
        # If only one course selected
        if len(index) == 1:
            msg = "Do you want to remove the selected course? (" + tbl[index[0][0]].item(index[0][1])['values'][0] + ")"
        # Else create msg prompt for batch delete courses
        else:
            msg = "Do you want to remove the selected course? ("
            for i in range(len(index)):
                msg = msg + tbl[index[i][0]].item(index[i][1])['values'][0]
                if i+1 != len(index):
                    msg+=", "
            msg = msg + ")"
        # If answer yes then proceed with course deletion
        response = messagebox.askquestion("askquestion", msg)
        for i in range(len(index)):
            self.tot_Removed += 1
            if response == 'yes':
                tbl[index[i][0]].delete(index[i][1])
                if type == 1:
                    self.edtMiTbls_iid -= 1
                else:
                    self.edtMjTbls_iid -= 1

    # Save major to the database
    def openMajor_editMajor_saveMajor(self, major):
        plan = []
        j = 0
        plan.append({'major': major})
        for i in range(0, 8):
            cnt = len(self.edtMjTbls[i].get_children())
            for course in range(cnt+self.tot_Removed):
                try:
                    self.edtMjTbls[i].item(course)
                    sub = ""
                    cat = ""
                    subcat = self.edtMjTbls[i].item(course)['values'][0].split()
                    try:
                        cat = subcat[1]
                        sub = subcat[0]
                    except IndexError as b:
                        sub = subcat[0]
                        cat = ""
                    plan.append([{ 'semester': i+1}, {"course" : {
                        'subject': sub,
                        'catalog': cat,
                        'title': self.edtMjTbls[i].item(course)['values'][1],
                        'credit': self.edtMjTbls[i].item(course)['values'][2]
                    }} ])
                    j+=1
                except TclError as b:
                    continue
        pub.sendMessage("save_maj_plan", obj=plan)

    # Creates window when user wants to make a new major from the menu
    def newMajorButton(self):
        self.newMajorWindow = Toplevel(self.mainwin)
        self.newMajorWindow.wm_title("New Major")
        self.newMajorWindow.geometry("350x150")
        self.newMajorWindow.resizable(width=0, height=0)
        self.newMajorWindow.attributes('-topmost', 'true')
        self.mainwin.eval(f'tk::PlaceWindow {str(self.newMajorWindow)} center')

        newMajorFrame = Frame(self.newMajorWindow)
        newMajorFrame.pack(padx=50, pady=10)

        buttonFrame = Frame(self.newMajorWindow)
        buttonFrame.pack(padx=50, pady=10)

        newMajorEntryLbl = Label(newMajorFrame, text='Major:')
        newMajorEntryLbl.pack(side=LEFT)
        newMajorEntry = Entry(newMajorFrame, width=200)
        newMajorEntry.pack(side=LEFT)

        newB = Button(buttonFrame, text='Create',
                         command=lambda: self.openMajorButton(newMajorEntry.get(), True))
        newB.pack()
    # Opens a major
    def openMajorButton(self, major, new):
        if new == False:
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
        else:
            self.close(self.addEditMajorWindow)
            self.schedule.entryconfigure(1, state=NORMAL)
            self.editMajorWindow = Toplevel(self.mainwin)
            self.editMajorWindow.geometry("1150x850")
            self.editMajorWindow.wm_title("Edit Major")
            self.editMajorWindow.attributes('-topmost', 'true')

        treeviewFrame = Frame(self.editMajorWindow)
        treeviewFrame.pack(fill=BOTH, expand=True)
        addCrsBtnFrame = Frame(self.editMajorWindow)
        addCrsBtnFrame.pack()

        self.edtMjLbls = []
        self.edtMjTbls = []

        addCourseBtn = Button(addCrsBtnFrame, text="Add course", command=lambda: self.planningWorksheet_editMajor_addCourseButton(self.editMajorWindow, 0))
        rmvCourseBtn = Button(addCrsBtnFrame, text="Remove course", command=lambda: self.openMajor_editMajor_delCourseButton(0))
        savePlanBtn = Button(addCrsBtnFrame, text="Save Plan", command=lambda: self.openMajor_editMajor_saveMajor(major))

        addCourseBtn.pack(side=LEFT, padx=10)
        rmvCourseBtn.pack(side=LEFT, padx=10)
        savePlanBtn.pack(side=RIGHT, padx=10)

        # Treeviews are created
        self.createTable(treeviewFrame, self.edtMjLbls, self.edtMjTbls, 8)

        # Filling semesters for major
        semsIndex = 0
        for sem in self.majorsFYP:
            self.edtMjTbls_iid = 0
            for course in sem:
                self.edtMjTbls[semsIndex].insert(parent='', index='end',
                                                              iid=self.edtMjTbls_iid,
                                                              values=(course[1] + " " + course[2], course[3], course[4]))
                self.edtMjTbls_iid += 1
            semsIndex += 1

    # Add Major Button from Update DB
    def addEditMajor(self):
        self.addEditMajorWindow = Toplevel(self.mainwin)
        self.addEditMajorWindow.wm_title("Edit/Add Major")
        self.addEditMajorWindow.geometry("300x310")
        self.addEditMajorWindow.resizable(width=0, height=0)
        self.addEditMajorWindow.attributes('-topmost', 'true')
        self.mainwin.eval(f'tk::PlaceWindow {str(self.addEditMajorWindow)} center')
        pub.sendMessage("request_Major_Plan")  # Retrieves list of majors from database
        self.majors.sort()

        # Filters the majors for the student box when typing in the entry fields
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

        searchB = Button(btnFrame, text='New',
                         command=lambda: self.newMajorButton())
        searchB.pack()

        majorEntryLbl = Label(majorFrame, text='Major:')
        majorEntryLbl.pack(side=LEFT)
        majorEntry = Entry(majorFrame, width=200)
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


        searchB = Button(btnFrame, text='Open', command=lambda: self.openMajorButton(self.majorBox.get(self.majorBox.curselection()), False))
        searchB.pack()
        """
        self.frame.bind("<Return>",
                        lambda event, a=10, b=20, c=30:
                        self.rand_func(a, b, c))
        """

    # Opens a minor
    def openMinorButton(self, minor):
        if self.minorBox.get(self.minorBox.curselection()) != "":
            self.close(self.addEditMinorWindow)
            pub.sendMessage("request_MinorAddEdit", minor=minor)
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

        addCrsBtnFrame = Frame(editMinorWindow)
        addCrsBtnFrame.pack()

        self.edtMiLbls = []
        self.edtMiTbls = []

        addCourseBtn = Button(addCrsBtnFrame, text="Add course",
                              command=lambda: self.planningWorksheet_editMajor_addCourseButton(editMinorWindow, 1))
        rmvCourseBtn = Button(addCrsBtnFrame, text="Remove course",
                              command=lambda: self.openMajor_editMajor_delCourseButton(1))
        savePlanBtn = Button(addCrsBtnFrame, text="Save Plan",
                             command=lambda: self.openMajor_editMajor_saveMajor(minor))

        addCourseBtn.pack(side=LEFT, padx=10)
        rmvCourseBtn.pack(side=LEFT, padx=10)
        savePlanBtn.pack(side=RIGHT, padx=10)

        # Treeviews are created
        cnt = len(self.minorsFYP)
        self.createTable(editMinorFrame, self.edtMiLbls, self.edtMiTbls, cnt)

        # Filling semesters for major
        semsIndex = 0
        for sem in self.minorsFYP:
            self.edtMiTbls_iid = 0
            for course in sem:
                self.edtMiTbls[semsIndex].insert(parent='', index='end',
                                                 iid=self.edtMiTbls_iid,
                                                 values=(course[1] + " " + course[2], course[3], course[4]))
                self.edtMiTbls_iid += 1
            semsIndex += 1

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
        # Filters the minors out for minorbox
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
        minorEntry = Entry(minorFrame, width=200)
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

        searchB = Button(btnFrame, text='Open', command=lambda: self.openMinorButton(self.minorBox.get(self.minorBox.curselection())))
        searchB.pack()

    # Delete major in Update DB
    def delMajor(self):
        t = Toplevel(self.mainwin)
        t.wm_title("Delete Major")
        t.geometry("400x325")
        t.resizable(width=0, height=0)
        t.attributes('-topmost', 'true')
        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')
        pub.sendMessage("request_ListMajors")

        # Filters the majors
        def filtr(e):
            chars1 = fnameE.get()
            index = 0
            if chars1 != "":
                fltrdStu1 = [x for x in self.majors if chars1.lower() in x.lower()]
                self.majorsBox.delete(0, END)
                fltrdStu = list(fltrdStu1)

                for i in fltrdStu:
                    self.majorsBox.insert(END, fltrdStu[index])
                    index += 1
            else:
                self.majorsBox.delete(0, END)
                for i in self.majors:
                    self.majorsBox.insert(END, self.majors[index])
                    index += 1
        # Fills entries when typing in the entry fields
        def fillEntry(e):
            if self.majorsBox.curselection() != "":
                selectedMajor = self.majorsBox.get(self.majorsBox.curselection())
                selectedMajorSplit = selectedMajor.split()

                fnameE.delete(0, END)

                fnameE.insert(0, selectedMajorSplit[0])
        # Closes a window
        def close(e):
            self.DB.entryconfigure(5, state=NORMAL)
            t.destroy()

        t.bind('<Destroy>', close)
        self.DB.entryconfigure(5, state=DISABLED)

        # Delete major
        def deleteMajorButton():  # Delete the major from database
            name = fnameE.get()
            if name != "" and id != "":
                pub.sendMessage("request_DelMajor", acad=name)
                self.DB.entryconfigure(5, state=NORMAL)
                t.destroy()

        nameFrame = Frame(t)
        nameFrame.pack(side=TOP, anchor='w', padx=20, pady=10)

        label2 = Label(nameFrame, text='Major Abbreviation:').pack(side=LEFT)
        fnameE = Entry(nameFrame, width=15)
        fnameE.pack(side=TOP)
        fnameE.bind("<KeyRelease>", filtr)

        majorsFrame = LabelFrame(t, text="Students")
        majorsFrame.pack(side=TOP, anchor=CENTER)

        self.majorsVar = self.majors

        self.majorsBox = Listbox(majorsFrame, selectmode=SINGLE, justify=CENTER, exportselection=False,
                                 listvariable=self.majorsVar, height=10, width=3500, font=('Helvetica', 12))
        self.majorsBox.pack(side=TOP)
        # self.studentBox.bind("<Double-Button-1>", openScheduleSearchButton)

        self.majorsBox.bind("<<ListboxSelect>>", fillEntry)
        self.majorsBox.delete(0, END)

        self.majors.sort()
        index = 0
        for i in self.majors:
            self.majorsBox.insert(END, self.majors[index])
            index += 1

        butFrame = Frame(t)
        butFrame.pack(side=BOTTOM, anchor=CENTER, pady=10)
        searchB = Button(butFrame, text='Delete', command=deleteMajorButton)
        searchB.pack()

    # Delete Minor in Update DB
    def delMinor(self):
        t = Toplevel(self.mainwin)
        t.wm_title("Delete Minor")
        t.geometry("400x325")
        t.resizable(width=0, height=0)
        t.attributes('-topmost', 'true')
        self.mainwin.eval(f'tk::PlaceWindow {str(t)} center')
        pub.sendMessage("request_ListMinors")
        # Filters minors
        def filtr(e):
            chars1 = fnameE.get()
            index = 0
            if chars1 != "":
                fltrdStu1 = [x for x in self.minors if chars1.lower() in x.lower()]
                self.minorsBox.delete(0, END)
                fltrdStu = list(fltrdStu1)

                for i in fltrdStu:
                    self.minorsBox.insert(END, fltrdStu[index])
                    index += 1
            else:
                self.minorsBox.delete(0, END)
                for i in self.minors:
                    self.minorsBox.insert(END, self.minors[index])
                    index += 1
        # Fills entry
        def fillEntry(e):
            if self.minorsBox.curselection() != "":
                selectedMinor = self.minorsBox.get(self.minorsBox.curselection())
                selectedMinorSplit = selectedMinor.split()

                fnameE.delete(0, END)

                fnameE.insert(0, selectedMinorSplit[0])
        # Closes window
        def close(e):
            self.DB.entryconfigure(6, state=NORMAL)
            t.destroy()

        t.bind('<Destroy>', close)
        self.DB.entryconfigure(6, state=DISABLED)

        # Deletes minor button
        def deleteMinorButton():  # Delete the minor from database
            name = fnameE.get()
            if name != "" and id != "":
                pub.sendMessage("request_DelMinor", acad=name)
                self.DB.entryconfigure(6, state=NORMAL)
                t.destroy()

        nameFrame = Frame(t)
        nameFrame.pack(side=TOP, anchor='w', padx=20, pady=10)

        label2 = Label(nameFrame, text='Major Abbreviation:').pack(side=LEFT)
        fnameE = Entry(nameFrame, width=15)
        fnameE.pack(side=TOP)
        fnameE.bind("<KeyRelease>", filtr)

        minorsFrame = LabelFrame(t, text="Students")
        minorsFrame.pack(side=TOP, anchor=CENTER)

        self.minorsVar = self.majors

        self.minorsBox = Listbox(minorsFrame, selectmode=SINGLE, justify=CENTER, exportselection=False,
                                 listvariable=self.minorsVar, height=10, width=3500, font=('Helvetica', 12))
        self.minorsBox.pack(side=TOP)
        # self.studentBox.bind("<Double-Button-1>", openScheduleSearchButton)

        self.minorsBox.bind("<<ListboxSelect>>", fillEntry)
        self.minorsBox.delete(0, END)

        self.minors.sort()
        index = 0
        for i in self.minors:
            self.minorsBox.insert(END, self.minors[index])
            index += 1

        butFrame = Frame(t)
        butFrame.pack(side=BOTTOM, anchor=CENTER, pady=10)

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
