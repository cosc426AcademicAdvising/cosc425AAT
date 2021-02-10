from tkinter import *
from tkinter import ttk

root = Tk()

main = Frame(root)
main.pack(fill=BOTH, expand=1)

recentFilesCanvas = Canvas(main)
recentFilesCanvas.pack(side=LEFT, fill=BOTH, expand=1)

scroll = ttk.Scrollbar(main, orient=VERTICAL, command=recentFilesCanvas.yview)
scroll.pack(side=RIGHT, fill=Y)

recentFilesCanvas.configure(yscrollcommand=scroll.set)
recentFilesCanvas.bind('<Configure>', lambda e: recentFilesCanvas.configure(scrollregion = recentFilesCanvas.bbox("all")))

frame2 = Frame(recentFilesCanvas)

recentFilesCanvas.create_window((0,0), window=frame2, anchor='nw')



for i in range (50):
    Label(frame2, text=f'entry {i} ').grid(row=i, column=0, padx=10, pady=10)

root.mainloop()
