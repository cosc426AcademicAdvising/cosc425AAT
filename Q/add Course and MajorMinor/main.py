import pymongo
import json

client = pymongo.MongoClient("mongodb+srv://COSC425AAT:ucciEcY4ItzL6BRN@cluster0.qmhln.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['COSC425AAT']

def addCourse():
    myCol = db.get_collection("Course")
    title = input("Type title of Course(ex. COSC 220)\t")
    descr = input("Enter a brief description of course(ex. Computer Science II)\t")
    cred = input("Enter number of credit hours\t")
    info = {
        "title": title,
        "descr": descr,
        "cred": cred,
    }
    myCol.insert_one(info)

def addMajMin():
    myCol = db.get_collection("Dept")
    name = input("Enter a the major/minor name\t")
    M_m = input("Type whether this is a Major or Minor\t")
    prog = input("Enter the academic program(ex. UNBSS)\t")
    school = input("Enter the short name of school(ex. Perdue)\t")
    fullSchool = input("Enter the full name of the school(ex Perdue School of Business)\t")
    info = {
        "Acad Plan": name,
        "Plan Type": M_m,
        "Acad Prog": prog,
        "School": school,
        "School Full Name": fullSchool
    }
    myCol.insert_one(info)

addCourse()
addMajMin()