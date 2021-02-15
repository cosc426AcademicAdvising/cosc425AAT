import tkinter as Tk


class View():
    def __init__(self, master, controller):
        self.controller = controller
        self.frame = Tk.Frame(master)
        self.frame.pack()
        self.viewPanel = ViewPanel(master, controller)


class ViewPanel():
    def __init__(self, root, controller):
        self.controller = controller

        # frame 1
        self.framePanel = Tk.Frame(root)
        self.framePanel.pack()

        self.label = Tk.Label(self.framePanel, text="Enter integer, click to add num")
        self.label.pack()

        self.v_num = Tk.StringVar()
        self.num = Tk.Label(self.framePanel, textvariable=self.v_num)
        self.num.pack()

        self.v_entry = Tk.StringVar()
        self.entry = Tk.Entry(self.framePanel, textvariable=self.v_entry)
        self.entry.pack()

        # frame 2
        self.framePanel2 = Tk.Frame(root)
        self.framePanel2.pack()

        self.btn = Tk.Button(self.framePanel2, text="10")
        self.btn.pack(side='left')
        # Event handlers passes events to controller
        self.btn.bind("<Button>", controller.add10)

        self.btn2 = Tk.Button(self.framePanel2, text="100")
        self.btn2.pack(side='left')
        # Event handlers passes events to controller
        self.btn2.bind("<Button>", controller.add100)
