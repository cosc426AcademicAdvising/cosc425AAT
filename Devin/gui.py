import tkinter as tk
from tkinter import *


# Blank sample button for other menu bar options
def donothing():
    hide_all_frames()
    filewin = Toplevel(root)
    button = Button(filewin, text="Do nothing button")
    button.pack()


############################################################
#   Menu bar functions
def new_schedule():
    filewin = Toplevel(root)
    button = Button(filewin, text="You clicked new schedule")
    button.place(relx=0, rely=0)


def open_schedule():
    filewin = Toplevel(root)
    button = Button(filewin, text="You clicked open schedule")
    button.place(relx=0, rely=0)


def save_schedule():
    filewin = Toplevel(root)
    button = Button(filewin, text="You clicked save schedule")
    button.place(relx=0, rely=0)


def delete_schedule():
    filewin = Toplevel(root)
    button = Button(filewin, text="You clicked delete schedule")
    button.place(relx=0, rely=0)


def export_schedule():
    filewin = Toplevel(root)
    button = Button(filewin, text="You clicked export schedule")
    button.place(relx=0, rely=0)


def recent_schedule():
    filewin = Toplevel(root)
    button = Button(filewin, text="You clicked recent schedule")
    button.place(relx=0, rely=0)


def print_schedule():
    filewin = Toplevel(root)
    button = Button(filewin, text="You clicked print schedule")
    button.place(relx=0, rely=0)


############################################################

############################################################
# Hides all frames on the screen

def hide_all_frames():
    frame.place_forget()
    background_label.place_forget()


############################################################
# Initialize GUI
root = tk.Tk()

canvas = tk.Canvas(root, height=650, width=1300)
canvas.pack()

frame = tk.Frame(root, bg='#8a0000')
frame.place(relwidth=1.0, relheight=1.0)

############################################################
# Set background image
bground_image = tk.PhotoImage(file='checklist.png')
background_label = tk.Label(frame, image=bground_image)
background_label.image= bground_image
background_label.place(relx=0.2, rely=0.18, relwidth=0.73, relheight=0.79)

############################################################
# Student Info Label

# random var
std_name = "Florent Dondjeu"
std_id = "1234567"
std_year = "Junior"
std_grad = "2030"

var = StringVar()

# Making label to hold student information
student_info_label = Label(frame, textvariable=var)
student_info_label.place(relx=0.3, rely=0.025, width=700, height=80)

# Indentation of student information
var.set(
    " " * 8 + "Name : " + std_name + '\n' +
    "Student ID : " + std_id + "\t" * 3 + "Grad. Yr : " + std_grad + '\n' +
    " " * 10 + "Year : " + std_year
)

############################################################
# Creating scroll bar and list for recent area
scrollbar = Scrollbar(frame)
scrollbar.place(relx=0.155, rely=0.025, relwidth=0.015, relheight=0.4)

recent_list = Listbox(frame, yscrollcommand=scrollbar.set)
# Filling list with schedules
for i in range(30):
    recent_list.insert(END, "Schedule " + str(i))

recent_list.place(relx=0.015, rely=0.025, relwidth=0.14, relheight=0.4)
# Connecting list and scrollbar functionality
scrollbar.config(command=recent_list.yview)

############################################################
# Create labels for different main screen aspects
# recent_label = tk.Label(frame, text="Recent Schedule", bg='white', fg='black')
# recent_label.place(relx=0.015, rely=0.025, relwidth=0.14, relheight=0.4)

selecte_label = tk.Label(frame, text="Selected Courses", bg='white', fg='black')
selecte_label.place(relx=0.015, rely=0.45, relwidth=0.14, relheight=0.5)

############################################################

############################################################
# Create different menu bar options for "Schedule" drop down menu
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New Schedule", command=new_schedule)
filemenu.add_command(label="Open Schedule", command=open_schedule)
filemenu.add_command(label="Save Schedule", command=save_schedule)
filemenu.add_command(label="Delete Schedule", command=delete_schedule)
filemenu.add_command(label="Export Schedule", command=export_schedule)
filemenu.add_command(label="Recent Schedules", command=recent_schedule)
filemenu.add_command(label="Print Schedule", command=print_schedule)

filemenu.add_separator()

filemenu.add_command(label="Clear Screen", command=hide_all_frames)
filemenu.add_command(label="Exit", command=root.quit)

############################################################

############################################################
# Create menu bar options for "Major" drop down menu
menubar.add_cascade(label="File", menu=filemenu)
schedmenu = Menu(menubar, tearoff=0)

schedmenu.add_command(label="Accounting", command=donothing)
schedmenu.add_command(label="Art", command=donothing)
schedmenu.add_command(label="Biology", command=donothing)
schedmenu.add_command(label="Chemistry", command=donothing)
schedmenu.add_command(label="Communication", command=donothing)
schedmenu.add_command(label="Computer Science", command=donothing)

############################################################

############################################################
# Create menu bar options for "Help" drop down menu
menubar.add_cascade(label="Major", menu=schedmenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Menu", command=donothing)
helpmenu.add_command(label="About", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

############################################################

root.config(menu=menubar)

root.mainloop()
