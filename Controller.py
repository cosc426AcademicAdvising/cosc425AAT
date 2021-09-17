from View import View
from Model import Model
from tkinter import *
# from tkinter import ttk
from pubsub import pub

class Controller:
    def __init__(self, master):
        self.model = Model()
        self.view = View(master)

        pub.subscribe(self.newSchedule, "New Menu Dropdown Pressed")

        # for populating planning worksheet
        pub.subscribe(self.planningWorksheet_open, "request_PPW")
        pub.subscribe(self.view.planningWorksheet_fill, "PPW_information")
        pub.subscribe(self.addCourse, "request_course#")
        pub.subscribe(self.findStudents, "requestStudents")
        pub.subscribe(self.view.openSchedule, "listOfStudents")

        # for populating Four Year Plan
        # pub.subscribe(self.fourYearPlan_open, "request_FYP")
        pub.subscribe(self.view.fourYearPlan_fill, "PPW_information")

        # for refreshing the four year plan
        pub.subscribe(self.model.getFourYear_refresh, "refresh_fyp")
        pub.subscribe(self.view.fourYearPlan_refresh, "FYP_refresh_info")

        # for specific mojor and minor under a school
        pub.subscribe(self.setMajor, "request_major")
        pub.subscribe(self.setMinor, "request_minor" )

        pub.subscribe(self.setSchools, "request_allSchools")
        pub.subscribe(self.setSubjects, "request_allSubjects")

        # for saving info from program planning sheet
        pub.subscribe(self.saveSchedule, "save_schedule")

        pub.subscribe(self.openPPW, "request_CSV")
        pub.subscribe(self.exportSchedule, "export_schedule")

        pub.subscribe(self.model.delMajor, "request_DelMajor")
        pub.subscribe(self.model.delMinor, "request_DelMinor")
        pub.subscribe(self.model.addMajor, "request_AddMajor")
        pub.subscribe(self.model.addMinor, "request_AddMinor")

        pub.subscribe(self.model.setAuthToken, "request_setAuthToken")

    def newSchedule(self):
        self.schedule = Toplevel()
        self.schedule.geometry('1000x600')
        # Need to fill title with name of student from database
        self.schedule.title("Insert Person Name Here")
        # Need to send information from database to this new window

    def fourYearPlan_open(self, name, id):
        # self.model.getStudent("Bob Robert", "7654321")
        self.model.getStudent(name, id)

    def planningWorksheet_open(self, name, id):
        # self.model.getStudent("Bob Robert", "7654321")
        self.model.getStudent(name, id)

    def addCourse(self, sub, cat):
        self.view.addCourseSearchResult = list( self.model.getCoursebySubCat(sub.upper(), cat))

    def findStudents(self):
        self.view.studentsVar = self.model.getAllStudents().copy()
        self.view.studentIdsVar = self.model.getAllStudentIds().copy()

    def setMajor(self, sch):
        self.view.majorVar.set( self.model.getMajorsbySchool(sch) )

    def setMinor(self, sch):
        self.view.minorVar.set( self.model.getMinorsbySchool(sch) )

    def setSchools(self):
        self.view.schList = self.model.getSchools()

    def setSubjects(self):
        self.view.subjectsList = self.model.getSubjects()

    def saveSchedule(self, obj):
        self.model.updateStudent(obj)

    def openPPW(self):
        self.model.openCSV()

    def exportSchedule(self, id, fname):
        self.model.mkPdf(id, fname)

if __name__=="__main__":
    root = Tk()
    app = Controller(root)
    root.mainloop()

