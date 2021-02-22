from View import View
from Model import Model

from tkinter import *
from tkinter import ttk
from pubsub import pub


class Controller:
    def __init__(self, master):
        self.view = View(master)
        self.model = Model()
        #self.newSchedule(master)
        # pub.subscribe(pub.sendMessage("New Window", master), "New Menu Dropdown Pressed")
        # pub.subscribe(newSchedule, "New Window")
        pub.subscribe(self.newSchedule, "New Menu Dropdown Pressed")

    def newSchedule(self):
        self.schedule = Toplevel()
        self.schedule.geometry('1000x600')
        # Need to fill title with name of student from database
        self.schedule.title("Insert Person Name Here")
        # Need to send information from database to this new window

if __name__=="__main__":
    root = Tk()
    app = Controller(root)
    root.mainloop()