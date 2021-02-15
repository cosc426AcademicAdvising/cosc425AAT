import tkinter as tk
from tkinter import *


# from pubsub import pub  # message passing between MVC


class View:
    def __init__(self, parent):
        # initialize variables
        self.container = parent
        self.flagLoadImage = FALSE
        self.hut_width = 40
        self.hut_height = 56

    def setup(self):
        # run first
        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        # setup frames
        self.var = tk.IntVar()
        self.background_label = tk.Label(self.container)
        self.topFrame = Frame(self.container, borderwidth=2, highlightbackground="black", highlightcolor="red",
                              highlightthickness=1, width=300, height=600)
        self.bottomFrame = Frame(self.container, borderwidth=2, highlightbackground="black", highlightcolor="red",
                                 highlightthickness=1, width=500, height=600)
        self.topFrame2 = Frame(self.topFrame)
        # button
        self.b1LoadImg = tk.Button(self.topFrame2, text="Load Image", command=self.loadImg)
        self.b2LineDetect = tk.Button(self.topFrame2, text="Line Detection", command=self.lineDetect)
        # scale bar
        self.scale1 = tk.Scale(self.topFrame, from_=1, to=20, orient=HORIZONTAL, length=500, label='pixel',
                               command=self.scalerChange)
        self.scale1.set(1)
        self.scale2 = tk.Scale(self.topFrame, from_=1, to=130, orient=HORIZONTAL, length=500, label='threshold',
                               command=self.scalerChange)
        self.scale2.set(50)
        self.scale3 = tk.Scale(self.topFrame, from_=1, to=500, orient=HORIZONTAL, length=500, label='mini line length',
                               command=self.scalerChange)
        self.scale3.set(10)
        self.scale4 = tk.Scale(self.topFrame, from_=1, to=100, orient=HORIZONTAL, length=500, label='max line gap',
                               command=self.scalerChange)
        self.scale4.set(50)
        # image panel
        self.panelA = tk.Label(self.bottomFrame, text='image here')

    def setup_layout(self):
        self.topFrame.pack(side=TOP)
        self.bottomFrame.pack(side=BOTTOM)
        self.topFrame2.pack(side=TOP)
        self.b1LoadImg.pack(side=LEFT)
        self.b2LineDetect.pack(side=RIGHT)
        self.scale4.pack(side=BOTTOM)  # max line gap
        self.scale3.pack(side=BOTTOM)  # min line length
        self.scale2.pack(side=BOTTOM)  # threshold
        self.scale1.pack(side=BOTTOM)  # pixel
        self.panelA.pack()

    def loadImg(self):
        print("loadImg")

    def lineDetect(self):
        print("lineDetect")

    def scalerChange(self, val):
        print("scaler change")


# test run
if __name__ == "__main__":
    mainwin = tk.Tk()
    WIDTH = 800
    HEIGHT = 600
    mainwin.geometry("%sx%s" % (WIDTH, HEIGHT))
    # mainwin.resizable(0, 0)
    mainwin.title("Open CV")

    view = View(mainwin)
    view.setup()
    mainwin.mainloop()
