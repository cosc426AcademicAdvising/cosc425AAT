from tkinter.filedialog import askopenfilename
import json
from pubsub import pub      # pip install PyPubSub
import pymongo

client = pymongo.MongoClient("mongodb+srv://COSC425AAT:ucciEcY4ItzL6BRN@cluster0.qmhln.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['COSC425AAT']

class Model:
    def __init__(self):
        return

    def listAllMajors(self):
        myCol = db.get_collection('Department')
        obj = myCol.find({'Plan Type': 'Major'})
        majors = []
        for i in obj:
            majors.append(i['Acad Plan'])
        return majors

    def listAllMinors(self):
        myCol = db.get_collection('Department')
        obj = myCol.find({'Plan Type': 'Minor'})
        minors = []
        for i in obj:
            minors.append(i['Acad Plan'])
        return minors
    # Displays what prereqs are necessary for a subject + catalog
    def getPreReq(subject, catalog):
        myCol = db.get_collection('Course')
        obj = myCol.find_one({'$and': [{'Subject': subject}, {'Catalog': catalog}]})
        print(obj['RQ Descr(Descrlong)'])

    sub = input("Enter subject")
    cat = input("Enter catalog")
    getPreReq(sub, cat)

    def openJson(self):
        path = askopenfilename(
            initialdir="./",
            filetypes=[("JSON File", "*.json"), ("All Files", ".")],
            title="Choose a Student Schedule file")

        if len(path) > 0:
            with open(path) as f:
                data = json.load(f)
        else:
            return

        numbCourses = len(data['taking_course'])
        cred = 0
        courses = []
        backup = []
        for c in data['taking_course']:
            courseID = [c['subject'], c['catalog']]
            courses.append((courseID, c['title'], c['cred'], c['genED']))
            cred += c['cred']

        for c in data['backup_course']:
            courseID = [c['subject'], c['catalog']]
            backup.append((courseID, c['title'], c['cred'], c['genED']))

        pub.sendMessage("PPW_information", arg1=data, arg2=cred, arg3=courses, arg4=numbCourses, arg5=backup)

