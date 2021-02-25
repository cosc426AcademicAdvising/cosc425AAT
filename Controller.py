from View import View
from Model import Model

from tkinter import *
from pubsub import pub


class Controller:
    def __init__(self, master):
        self.view = View(master)
        self.model = Model()

        #self.newSchedule(master)
        # pub.subscribe(pub.sendMessage("New Window", master), "New Menu Dropdown Pressed")
        # pub.subscribe(newSchedule, "New Window")

        pub.subscribe(self.newSchedule, "New Menu Dropdown Pressed")

        # for populating planning worksheet
        pub.subscribe(self.openPPW,"request_PPW")
        pub.subscribe(self.fillInfo,"PPW_information")

    def newSchedule(self):
        self.schedule = Toplevel()
        self.schedule.geometry('1000x600')
        # Need to fill title with name of student from database
        self.schedule.title("Insert Person Name Here")
        # Need to send information from database to this new window

    def openPPW(self):
        self.model.openJson()

    def fillInfo(self, arg1):
        # delete what was previously there then insert
        self.view.nameEntry.delete(0,END)
        self.view.nameEntry.insert(END, arg1[0])

        self.view.idEntry.delete(0,END)
        self.view.idEntry.insert(END, arg1[1])



if __name__=="__main__":
    root = Tk()
    app = Controller(root)
    root.mainloop()