from tkinter.filedialog import askopenfilename
import json
from pubsub import pub  # pip install PyPubSub
import pymongo
from reportlab.pdfgen.canvas import Canvas
from bson.regex import Regex

client = pymongo.MongoClient(
    "mongodb+srv://COSC425AAT:ucciEcY4ItzL6BRN@cluster0.qmhln.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
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
    def getPreReq(self, subject, catalog):
        myCol = db.get_collection('Course')
        obj = myCol.find_one({'$and': [{'Subject': subject}, {'Catalog': catalog}]})
        print(obj['RQ Descr(Descrlong)'])

    def getSubjects(self):
        myCol = db.get_collection('Catalog')
        obj = myCol.distinct('Subject')
        return obj

    def getStudent(self, sname, sid):
        myCol = db.get_collection('Student')
        # obj2 = myCol.aggregate([{u"$project": {u"count": {u"$size": u"$course_taken"}}}])
        # for i in obj2:
        #    cnt = int(i['count'])
        obj = myCol.find_one({'$and': [{'name': str(sname)}, {'s_id': int(sid)}]})
        numbCourses = 0
        cred = 0
        courses = []
        backup = []
        fourList = []
        for c in obj['taking_course']:
            courseID = c['subject'] + " " + c['catalog']
            courses.append((courseID, c['title'], c['cred'], c['genED']))
            cred += c['cred']

        for c in obj['backup_course']:
            courseID = c['subject'] + " " + c['catalog']
            backup.append((courseID, c['title'], c['cred'], c['genED']))

        courseHist = []  # four year plan list (return value)
        sem = "1"  # Keeps track of which semester in database
        total = 0  # Total number of semesters
        ctotal = 0  # Total number of courses in a semester

        myCol = db.get_collection('Student')

        # Gets total number of semesters through error handling
        for j in range(15):  # Max of 15 possible semesters taken
            stri = "semester_"  # Append which semester to string
            stri = stri + sem
            try:  # Error checks is semester is out of range
                (obj['course_taken'][0][stri])  # Sets the total to the currently viewed semester
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
                    (obj['course_taken'][0][stri][l])
                    ctotal = l + 1  # Sets total number of courses to currently viewed course
                    resl = [k, obj['course_taken'][0][stri][l]['subject'], obj['course_taken'][0][stri][l]['catalog'],
                            obj['course_taken'][0][stri][l]['title'],
                            obj['course_taken'][0][stri][l]['credits'], obj['course_taken'][0][stri][l][
                                'grade']]  # Creates a string value of each objects within array
                    courseList.append(resl)  # Appends that string to a course list
                    numbCourses = numbCourses + 1
                except IndexError as d:
                    ctotal = ctotal  # Last none index error course number is stored
            # print(ctotal)
            courseHist.append(courseList)

        fourList = self.getFourYear(obj['major'])

        pub.sendMessage("PPW_information", obj=obj, tcred=cred, courses=courses, numbCourse=numbCourses,
                        bcourses=backup, courseHist=courseHist, fourYear=fourList,
                        policies=self.getPolicies(obj['major']))

    def delStud(self, id):
        stud = db.get_collection('Student')
        query = {}
        query["s_id"] = int(id)
        info = stud.delete_many(query)
        if (info.deleted_count == 1):
            return "one entry deleted"
        elif (info.deleted_count == 0):
            return "no matches found, deleted 0 entries"
        else:
            return (str(info.deleted_count) + " entries deleted")

    def delCrs(self, sub, num):
        query = {}
        query["Subject"] = sub
        crs = db.get_collection('Course')
        # this ".*string.*" regex searches for entries containing the given string
        # when searching for a given catalog num normally, the entire string must match
        # a portion of the entries in the db have spaces at the beginning of the catalog num string
        # this regex ignores that space and is true if the field contains the given number anywhere in the string
        query["Catalog"] = Regex(u".*{0}.*".format(num), "i")
        info = crs.delete_many(query)
        if (info.deleted_count == 1):
            return "one entry deleted"
        elif (info.deleted_count == 0):
            return "no matches found, deleted 0 entries"
        else:
            return (str(info.deleted_count) + " entries deleted")

    def delDept(self, acad):
        dept = db["Department"]
        query = {"Subject": acad}
        info = dept.delete_many(query)
        if info.deleted_count == 1:
            return "one entry deleted"
        elif info.deleted_count == 0:
            return "no matches found, deleted 0 entries"
        else:
            return str(info.deleted_count) + " entries deleted"

    def pullStud(self, id, fname):
        client = pymongo.MongoClient(
            "mongodb+srv://COSC425AAT:ucciEcY4ItzL6BRN@cluster0.qmhln.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client['COSC425AAT']
        stud = db["Student"]
        query = {"s_id": id}
        curs = stud.find(query)
        data = {}
        for i in curs:
            data["name"] = i['name']
            data["s_id"] = i['s_id']
            try:
                data['major'] = i['major']
                data['dept'] = i['dept']
            except (TypeError, KeyError):
                data['major'] = 'Double major'
                multiMaj = 1
            try:
                data['major'] = i['major']
            except TypeError:
                data['major'] = i['major']
            data["status"] = i['status']
            data["year"] = i['year']
            data["credits"] = i['credits']
            data["sem_id"] = i['sem_id']
            data["registering_for"] = i['registering_for']
            data["enrll"] = i['enrll']
            data["advisor_mail"] = i['advisor_mail']
            data["memo"] = i['memo']
            data["course_taken"] = i['course_taken']
            data["taking_course"] = i['taking_course']
            data["backup_course"] = i['backup_course']
            with open(fname, 'w+') as f:
                json.dump(data, f, indent=4)

    def mkPdf(self, id, path):
        client = pymongo.MongoClient(
            "mongodb+srv://COSC425AAT:ucciEcY4ItzL6BRN@cluster0.qmhln.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client['COSC425AAT']
        stud = db["Student"]
        fyp = db["FourYear"]
        query = {"s_id": id}
        curs = stud.find(query)
        data = []
        canvas = Canvas(path, pagesize=(612.0, 792.0))
        major = ''
        multiMaj = 0
        for i in curs:
            data.append(i['name'])
            data.append(i['s_id'])
            try:
                data.append('major(s): ' + i['major'])
                data.append(i['dept'] + ' school')
            except (TypeError, KeyError):
                data.append("Double major")
                multiMaj = 1
            try:
                data.append('minor(s): ' + i['minor'])
            except TypeError:
                data.append("Double minor")
            data.append(i['status'])
            data.append(i['year'])
            data.append('current credits: ' + str(i['credits']))
            data.append(i['sem_id'])
            data.append('Registering for ' + i['registering_for'] + ' semester')
            data.append(i['enrll'])
            data.append(i['advisor_mail'])
            major = i['major']

        data.append("-----------------------------------------")
        data.append("Current courses:")
        obj = stud.find_one({'s_id': id})
        for x in obj['taking_course']:
            data.append("       " + x['subject'] + " " + str(x['catalog']) + " " + x['title'] + " | " + str(
                x['cred']) + ' credits')

        data.append("-----------------------------------------")
        data.append("Backup courses:")
        for x in obj['backup_course']:
            data.append("       " + x['subject'] + " " + str(x['catalog']) + " " + x['title'] + " | " + str(
                x['cred']) + ' credits')

        if (not multiMaj):
            data.append("-----------------------------------------")
            data.append("Four year plan:")
            obj2 = fyp.find_one({'major': major})
            for z in range(1, 16):
                try:
                    data.append("Semester {}".format(z))
                    for k in obj2['semester_{}'.format(z)]:
                        data.append("       " + k['subject'] + " " + str(k['catalog']) + " " + k['title'] + " | " + str(
                            k['credits']) + ' credits')
                    data.append("")
                except KeyError:
                    data.pop()
                    break

        x = 72
        y = 725
        for z in range(len(data)):
            canvas.drawString(x, y, str(data[z]))
            y -= 20
            if (y <= 75):
                canvas.showPage()
                y = 725

        canvas.save()

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

        # fourList.append(i['policies'])

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