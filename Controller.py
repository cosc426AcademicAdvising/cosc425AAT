from View import View
from Model import Model
from tkinter import *
# from tkinter import ttk
from pubsub import pub

class Controller:
    def __init__(self, master):
        self.model = Model()
        self.view = View(master, self.model.getSchools(), self.model.getSubjects())

        pub.subscribe(self.newSchedule, "New Menu Dropdown Pressed")

        # for populating planning worksheet
        pub.subscribe(self.planningWorksheet_open,"request_PPW")
        pub.subscribe(self.view.planningWorksheet_fill,"PPW_information")
        pub.subscribe(self.addCourse, "request_course#")

        # for populating Four Year Plan
        # pub.subscribe(self.fourYearPlan_open, "request_FYP")
        pub.subscribe(self.view.fourYearPlan_fill, "PPW_information")

        # for specific mojor and minor under a department
        pub.subscribe(self.setMajorMinor, "request_major_minor")

        # for saving info from program planning sheet
        pub.subscribe(self.saveSchedule, "save_schedule")

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

    def setMajorMinor(self, dep):
        self.view.majorList = list( self.model.getMajorsbySchool(dep) )
        self.view.minorList = list( self.model.getMinorsbySchool(dep) )

    def saveSchedule(self, obj):
        print("From controller: ", obj)

if __name__=="__main__":
    root = Tk()
    app = Controller(root)
    root.mainloop()

