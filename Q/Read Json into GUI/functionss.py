import pymongo
import json

client = pymongo.MongoClient("mongodb+srv://COSC425AAT:ucciEcY4ItzL6BRN@cluster0.qmhln.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['COSC425AAT']

def getNumCoursetoTake():
    myCol = db.get_collection('Student')
    obj = myCol.aggregate([{u"$project": {u"count": {u"$size": u"$taking_course"}}}])
    for i in obj:
        y = int(i['count'])
    return y
    
    
def genCoursetoTakeArr():
    f = open('stud.json', 'r')
    data = json.loads(f.read())
    corAr = []
    for i in data:

   # obj = myCol.find({'s_id': 1234567})

        for j in range(4):
            corAr.append((i['taking_course'][j]['course_num'], i['taking_course'][j]['course_title'], i['taking_course'][j]['course_cred'], i['taking_course'][j]['course_genED']))
    return corAr

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

def searchStudent():
    myCol = db.get_collection('Student')
    obj = myCol.find({'s_id': 1234567})
    for i in obj:
        return i

def loadJsonFile():
    f = open('stud.json', 'r')
    data = json.loads(f.read())

    for i in data:
        return i
