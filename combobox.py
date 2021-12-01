import pymongo
import json
from tkinter import *
from tkinter import ttk

client = pymongo.MongoClient("mongodb+srv://COSC425AAT:ucciEcY4ItzL6BRN@cluster0.qmhln.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['COSC425AAT']

def getSchools():
    myCol = db.get_collection("Department")
    schools = myCol.distinct('School')
    return schools

def getMajorsbySchool(schools):
    majList = []
    myCol = db.get_collection("Department")
    obj = myCol.find({"$and": [{"School": schools, "Plan Type": "Major"}]})
    for i in obj:
        majList.append(i['Acad Plan'])
    return  majList

def getMinorsbySchool(schools):
    minList = []
    myCol = db.get_collection("Department")
    obj = myCol.find({"$and": [{"School": schools, "Plan Type": "Minor"}]})
    for i in obj:
        minList.append(i['Acad Plan'])
    return minList

schl = getSchools()
print(schl)

M1 = getMajorsbySchool(schl[0])
M2 = getMajorsbySchool(schl[1])
M3 = getMajorsbySchool(schl[2])
M4 = getMajorsbySchool(schl[3])
M5 = getMajorsbySchool(schl[4])
M6 = getMajorsbySchool(schl[5])
M7 = getMajorsbySchool(schl[6])
M8 = getMajorsbySchool(schl[7])

m1 = getMinorsbySchool(schl[0])
m2 = getMinorsbySchool(schl[1])
m3 = getMinorsbySchool(schl[2])
m4 = getMinorsbySchool(schl[3])
m5 = getMinorsbySchool(schl[4])
m6 = getMinorsbySchool(schl[5])
m7 = getMinorsbySchool(schl[6])
m8 = getMinorsbySchool(schl[7])
schl[0] = "Undecided"


def selectMajor(e):
    if myCombo.get() == schl[0]:
        majorCombo.config(value=M1)
        majorCombo.current(0)
        minorCombo.config(value=m1)
        minorCombo.current(0)
    if myCombo.get() == schl[1]:
        majorCombo.config(value=M2)
        majorCombo.current(0)
        minorCombo.config(value=m2)
        minorCombo.current(0)
    if myCombo.get() == schl[2]:
        majorCombo.config(value=M3)
        majorCombo.current(0)
        minorCombo.config(value=m3)
        minorCombo.current(0)
    if myCombo.get() == schl[3]:
        majorCombo.config(value=M4)
        majorCombo.current(0)
        minorCombo.config(value=m4)
        minorCombo.current(0)
    if myCombo.get() == schl[4]:
        majorCombo.config(value=M5)
        majorCombo.current(0)
        minorCombo.config(value=m5)
        minorCombo.current(0)
    if myCombo.get() == schl[5]:
        majorCombo.config(value=M6)
        majorCombo.current(0)
        minorCombo.config(value=m6)
        minorCombo.current(0)
    if myCombo.get() == schl[6]:
        majorCombo.config(value=M7)
        majorCombo.current(0)
        minorCombo.config(value=m7)
        minorCombo.current(0)
    if myCombo.get() == schl[7]:
        majorCombo.config(value=M8)
        majorCombo.current(0)
        minorCombo.config(value=m8)
        minorCombo.current(0)

root = Tk()
root.title('Practice')
root.geometry("500x500")

myCombo = ttk.Combobox(root, value=schl)
myCombo.current(0)
myCombo.pack(pady=20)

myCombo.bind("<<ComboboxSelected>>", selectMajor)

majorCombo = ttk.Combobox(root, value=[""])
majorCombo.current(0)
majorCombo.pack(pady=20)

minorCombo = ttk.Combobox(root, value=[""])
minorCombo.current(0)
minorCombo.pack(pady=20)

root.mainloop()