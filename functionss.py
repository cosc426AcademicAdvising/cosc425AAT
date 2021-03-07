import pymongo
import json

client = pymongo.MongoClient("mongodb+srv://COSC425AAT:ucciEcY4ItzL6BRN@cluster0.qmhln.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['COSC425AAT']

def listAllMajors():
    myCol = db.get_collection('Department')
    obj = myCol.find({'Plan Type': 'MAJ'})
    majors = []
    for i in obj:
        majors.append(i['Descr'])
    return majors

def listAllMinors():
    myCol = db.get_collection('Department')
    obj = myCol.find({'Plan Type': 'MIN'})
    minors = []
    for i in obj:
        minors.append(i['Descr'])
    return minors

def getPreReq(subject, catalog):
    myCol = db.get_collection('Course')
    obj = myCol.find({'Subject': subject}, {'Catalog': catalog})
    for i in obj:
        print(i)
