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
    
    def getSchools(self):
        myCol = db.get_collection("Department")
        schools = myCol.distinct('School')
        return schools

    def getMajorsbySchool(self, schools):
        majList = []
        myCol = db.get_collection("Department")
        obj = myCol.find({"$and": [{"School": schools, "Plan Type": "Major"}]})
        for i in obj:
            majList.append(i['Acad Plan'])
        return majList

    def getMinorsbySchool(self, schools):
        minList = []
        myCol = db.get_collection("Department")
        obj = myCol.find({"$and": [{"School": schools, "Plan Type": "Minor"}]})
        for i in obj:
            minList.append(i['Acad Plan'])
        return minList

    # Get a course by searching for subject and catalog
    def getCoursebySubCat(self, sub, cat):
        myCol = db.get_collection('Course')
        spacer = " "
        newCat = spacer + cat
        obj = myCol.find_one({'$and': [{'Subject': sub}, {'Catalog': newCat}]})
        courseInfo = []
        courseInfo.append(obj['Subject'])
        courseInfo.append(obj['Catalog'])
        courseInfo.append(obj['Long Title'])
        courseInfo.append(obj['Allowd Unt'])
        return courseInfo

    # Displays what prereqs are necessary for a subject + catalog
    def getPreReq(subject, catalog):
        myCol = db.get_collection('Course')
        obj = myCol.find_one({'$and': [{'Subject': subject}, {'Catalog': catalog}]})
        print(obj['RQ Descr(Descrlong)'])

    def getSubjects(self):
        myCol = db.get_collection('Catalog')
        obj = myCol.distinct('Subject')
        return obj

    def getStudent(self, sname, sid):
        myCol = db.get_collection('Student')
        obj2 = myCol.aggregate([{u"$project": {u"count": {u"$size": u"$course_taken"}}}])
        for i in obj2:
            cnt = int(i['count'])
        obj = myCol.find_one({'$and': [{'name': str(sname)}, {'s_id': int(sid)}]})
        numbCourses = cnt
        cred = 0
        courses = []
        backup = []
        taken = []
        for c in obj['taking_course']:
            courseID = c['subject'] + " " + c['catalog']
            courses.append((courseID, c['title'], c['cred'], c['genED']))
            cred += c['cred']

        for c in obj['backup_course']:
            courseID = c['subject']+ " " +c['catalog']
            backup.append((courseID, c['title'], c['cred'], c['genED']))

        for c in obj['course_taken']:
            taken.append((c['subject'], c['catalog'], c['title'], c['cred'], c['genED'], c['grade']))

        fourList = self.getFourYear(obj['major'])

        pub.sendMessage("PPW_information", obj=obj, tcred=cred, courses=courses, numbCourse=numbCourses, bcourses=backup, courseHist=taken, fourYear=fourList, policies=self.getPolicies(obj['major']))

    def updateStudent(self, obj):
        myCol = db.get_collection('Student')
        stud = myCol.find_one({'s_id': int(obj['s_id'])})

        # Original total number of course student plans to take
        CTtotal = len(stud['taking_course'])

        # Original total number of courses student has for backups
        BUtotal = len(stud['backup_course'])

        # Iterate through each course a student plans to take and update the fields in the database
        for i in range(len(obj['taking_course'])):
            subcat = obj['taking_course'][i][0].split()
            field1 = "taking_course." + str(i) + ".subject"
            field2 = "taking_course." + str(i) + ".catalog"
            field3 = "taking_course." + str(i) + ".title"
            field4 = "taking_course." + str(i) + ".cred"
            field5 = "taking_course." + str(i) + ".genED"
            myCol.update_one({'s_id': int(obj['s_id'])},
                             {'$set': {
                                 field1: subcat[0],
                                 field2: subcat[1],
                                 field3: obj['taking_course'][i][1],
                                 field4: obj['taking_course'][i][2],
                                 field5: obj['taking_course'][i][3]
                             }}
                             )

        # Iterate through remaining courses and assign null value to subject indicating their need for removal
        for i in range(len(obj['taking_course']), CTtotal):
            field1 = "taking_course." + str(i) + ".subject"
            myCol.update_one({'s_id': int(obj['s_id'])},
                             {'$set': {
                                 field1: 'null'
                             }})

        # Iterate again through remaining courses and pull those courses from database that are no longer needed
        for i in range(len(obj['taking_course']), CTtotal):
            myCol.update_one({'s_id': int(obj['s_id'])},
                             {'$pull': {
                                 'taking_course': {'subject': 'null'}
                             }})

        # Iterate through each backup course and update the fields in the database
        for i in range(len(obj['backup_course'])):
            subcat = obj['backup_course'][i][0].split()
            field1 = "backup_course." + str(i) + ".subject"
            field2 = "backup_course." + str(i) + ".catalog"
            field3 = "backup_course." + str(i) + ".title"
            field4 = "backup_course." + str(i) + ".cred"
            field5 = "backup_course." + str(i) + ".genED"
            myCol.update_one({'s_id': int(obj['s_id'])},
                             {'$set': {
                                 field1: subcat[0],
                                 field2: subcat[1],
                                 field3: obj['backup_course'][i][1],
                                 field4: obj['backup_course'][i][2],
                                 field5: obj['backup_course'][i][3]
                             }}
                             )

        # Iterate through remaining courses and assign null value to subject indicating their need for removal
        for i in range(len(obj['backup_course']), BUtotal):
            field1 = "backup_course." + str(i) + ".subject"
            myCol.update_one({'s_id': int(obj['s_id'])},
                             {'$set': {
                                 field1: 'null'
                             }})

        # Iterate again through remaining courses and pull those courses from database that are no longer needed
        for i in range(len(obj['backup_course']), BUtotal):
            myCol.update_one({'s_id': int(obj['s_id'])},
                             {'$pull': {
                                 'backup_course': {'subject': 'null'}
                             }})

    def getPolicies(self, major):
        myCol = db.get_collection('FourYear')
        i = myCol.find_one({'major': major})
        return i['policies']

    def getFourYear(self, major):
        courseList = []  # course list
        fourList = []  # four year plan list (return value)
        sem = "1"  # Keeps track of which semester in database
        total = 0  # Total number of semesters
        ctotal = 0  # Total number of courses in a semester

        myCol = db.get_collection('FourYear')
        i = myCol.find_one({'major': major})

        #fourList.append(i['policies'])

        # Gets total number of semesters through error handling
        for j in range(15):  # Max of 15 possible semesters taken
            stri = "semester_"  # Append which semester to string
            stri = stri + sem
            try:  # Error checks is semester is out of range
                (i[stri])  # Sets the total to the currently viewed semester
                total = int(sem)
            except KeyError as b:
                total = total  # Last none KeyError semester is stored
            sem = str(int(sem) + 1)
        # print(total)

        for k in range(total):  # Iterates through each semester from previously calculated value
            stri = "semester_"  # Appends which semester to a string
            stri = stri + str(k + 1)
            # Gets total number of courses through error handling
            courseList = []
            for l in range(8):  # Max of 8 possible courses taken during any given semester

                try:  # Checks for Array index error
                    (i[stri][l])
                    ctotal = l + 1  # Sets total number of courses to currently viewed course
                    resl = [k, i[stri][l]['subject'], i[stri][l]['catalog'], i[stri][l]['title'],
                            i[stri][l]['credits']]  # Creates a string value of each objects within array
                    courseList.append(resl)  # Appends that string to a course list
                except IndexError as c:
                    ctotal = ctotal  # Last none index error course number is stored
            # print(ctotal)
            fourList.append(courseList)
        return fourList

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