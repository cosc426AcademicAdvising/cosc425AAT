from View import View
from Model import Model
import tkinter as tk
from pubsub import pub      # pip install PyPubSub


class Controller:
    def __init__(self, container):
        self.container = container
        self.model = Model()
        self.view = View(container)
        self.view.setup()

        # receive messages
        pub.subscribe(self.openSchedule, "request student info")    #(action, msg key)
        pub.subscribe(self.setVar,"student info sent")

    def openSchedule(self):
        print("student info request received")
        self.model.openSchedule()

    def setVar(self, arg1):
        print("receive student info from controller")
        self.view.setVar(arg1)

if __name__ == "__main__":
    root = tk.Tk()
    # root.geometry("%sx%s" % (1000, 600))
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))  # fills whole window
    root.title("Academic Advising Tool")

    app = Controller(root)
    root.mainloop()