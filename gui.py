from tkinter import *

# random var
std_name = "Florent Dondjeu"
std_id = "1234567"
std_year = "Junior"
std_grad = "2030"

root = Tk()

lframe = Frame(root, width=500, height=400)
lframe.pack(side=LEFT)

frame = Frame(root, width=500, height=400)
frame.pack(side=RIGHT)

student_info_frame = LabelFrame(frame, text="Student Information")
student_info_frame.place(width=425, height=90)

var = StringVar()
label = Label(student_info_frame, textvariable=var, justify=LEFT, padx=20)
var.set(" "*8 + "Name : " + std_name + '\n' +
        "Student ID : " + std_id + "\t"*3 + "Grad. Yr : " + std_grad + '\n' +
        " "*10 + "Year : " + std_year
        )
label.pack(anchor=NW)

root.mainloop()
