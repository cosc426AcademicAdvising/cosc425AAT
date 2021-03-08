from View import View
from Model import Model

from tkinter import *
from tkinter import ttk
from pubsub import pub


class Controller:
    def __init__(self, master):
        self.model = Model()
        self.view = View(master, self.model.listAllMajors(), self.model.listAllMinors())

        #self.newSchedule(master)
        # pub.subscribe(pub.sendMessage("New Window", master), "New Menu Dropdown Pressed")
        # pub.subscribe(newSchedule, "New Window")

        pub.subscribe(self.newSchedule, "New Menu Dropdown Pressed")

        # for populating planning worksheet
        pub.subscribe(self.openPPW,"request_PPW")
        pub.subscribe(self.view.populatePPW,"PPW_information")

    def newSchedule(self):
        self.schedule = Toplevel()
        self.schedule.geometry('1000x600')
        # Need to fill title with name of student from database
        self.schedule.title("Insert Person Name Here")
        # Need to send information from database to this new window

    def openPPW(self):
        self.model.getStudent("Bob Robert", 7654321)




if __name__=="__main__":
    root = Tk()
    app = Controller(root)
    root.mainloop()