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

    def getStudent(self, sname, sid):
        myCol = db.get_collection('Student')
        obj2 = myCol.aggregate([{u"$project": {u"count": {u"$size": u"$course_taken"}}}])
        for i in obj2:
            cnt = int(i['count'])
        obj = myCol.find_one({'$and': [{'name': sname}, {'s_id': sid}]})
        numbCourses = cnt
        cred = 0
        courses = []
        backup = []
        for c in obj['taking_course']:
            courseID = c['subject'] + " " + c['catalog']
            courses.append((courseID, c['title'], c['cred'], c['genED']))
            cred += c['cred']

        for c in obj['backup_course']:
            courseID = c['subject']+ " " +c['catalog']
            backup.append((courseID, c['title'], c['cred'], c['genED']))

        pub.sendMessage("PPW_information", arg1=obj, arg2=cred, arg3=courses, arg4=numbCourses, arg5=backup)

    def getFourYearLayout(sname, sid):
        myCol = db.get_collection('FourYear')
        crsList = []
        obj = myCol.distinct('four_year.semester', {'id': sid})
        for i in obj:
            crsList.append(i)
        print(crsList)

        fourList = []
        # For loop to iterate through all entries within the distinct list for comparison
        # Length of course list is number of distinct semesters for a certain student
        for x in range(len(crsList)):
            # aggregate pipeline
            pipe = myCol.aggregate([
                {
                    # unwind array for individual comparisons
                    '$unwind': '$four_year'
                },
                {
                    # match the semester with the distinct semester list
                    '$match': {'four_year.semester': crsList[x],
                               'id': sid,
                               'name': sname}
                },
                {
                    # group all values to a new object and get a count for total number of courses within
                    '$group': {'_id': '$four_year.semester',
                               'sub': {'$push': '$four_year.subject'},
                               'cat': {'$push': '$four_year.catalog'},
                               'tit': {'$push': '$four_year.title'},
                               'crd': {'$push': '$four_year.cred'},
                               # Number of courses within the semester
                               'count': {'$sum': 1}
                               }
                },

            ])
            # Outputs all objects returned by pipeline aggregate and appends them to a list
            # Through a double for loop iterating through the object and number of courses
            for i in pipe:
                val = i['count']
                for j in range(val):
                    str = [i['_id'], i['sub'][j], i['cat'][j], i['tit'][j], i['crd'][j]]
                    fourList.append(str)

        #How to access the elements within the list
        # 0 - Semester  1 - Subject  2 - Catalog  3 - Title  4 - Credits
        '''
        print('\n\n')
        for j in range(len(crsList)):
            print(crsList[j])
            for i in range(len(fourList)):
                if fourList[i][0] == crsList[j]:
                    print(fourList[i][1], fourList[i][2], fourList[i][3], fourList[i][4])
            print('\n')
        '''
        return fourList;

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

