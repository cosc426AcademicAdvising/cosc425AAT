import tkinter as tk
from tkinter import *


# from pubsub import pub  # message passing between MVC


class View:
    def _init_(self, parent):
        return

    def setup(self):
        # run first
        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        # setup frames
        self.topFrame = Frame(self.container, borderwidth=2, highlightedbackground="black", highlightedcolor="red",
                              highlightedthickness=1, width=500, height=600)
        self.topFrame2 = Frame(self.container, borderwidth=2, highlightedbackground="black", highlightedcolor="red",
                               highlightedthickness=1, width=500, height=600)
        self.bottomFrame = Frame(self.topFrame)
        # button
        self.b1loadImg = tk.Button(self.topFrame2, text="Load Image", command=self.loadImg)
        self.b2LineDetect = tk.Button(self.topFrame2, text="Line Detection", command=self.lineDetect)
        # scale bar

        # image panel

    def loadImg(self):
        print("loadImg")

    def lineDetect(self):
        print("lineDetect")

    # test run
    print("running view")
