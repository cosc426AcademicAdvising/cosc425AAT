from tkinter import *

# random var
std_name = "Florent Dondjeu"
std_id = "1234567"
std_year = "Junior"
std_grad = "2030"

root = Tk()
root.title("Academic Advising Tool")

# frame for menu
menu_frame = Frame(root, width=1000, height=25, bg='red')
menu_frame.pack(side=TOP)

# top frame
tframe = Frame(root, width=1000, height=50, bg='white')
tframe.pack(side=TOP)

# left frame
lframe = Frame(root, width=500, height=400, bg='green')
lframe.pack(side=LEFT)

# right frame
rframe = Frame(root, width=500, height=400)
rframe.pack(side=RIGHT)

# info frame inside right frame
student_info_frame = LabelFrame(rframe, text="Student Information")
student_info_frame.place(width=425, height=90)

var = StringVar()
label = abel(Lstudent_info_frame, textvariable=var, justify=LEFT, padx=20)
# concept output
var.set(
        " "*8 + "Name : " + std_name + '\n' +
        "Student ID : " + std_id + "\t"*3 + "Grad. Yr : " + std_grad + '\n' +
        " "*10 + "Year : " + std_year
        )
label.pack(anchor=NW)

root.mainloop()
