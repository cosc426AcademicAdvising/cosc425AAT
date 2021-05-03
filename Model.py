from tkinter.filedialog import askopenfilename
import json
import csv
from pubsub import pub  # pip install PyPubSub
import pymongo
from bson.regex import Regex
import re
import threading

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
            data["major"] = i['major']
            data["dept"] = i['dept']
            data['minor'] = i['minor']
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
            data["four_year"] = i['four_year']
            with open(fname, 'w+') as f:
                json.dump(data, f, indent=4)

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
        majList = []
        minList = []
        for c in obj['taking_course']:
            courseID = c['subject'] + " " + c['catalog']
            courses.append((courseID, c['title'], c['cred'], c['genED']))
            cred += c['cred']

        for c in obj['backup_course']:
            courseID = c['subject'] + " " + c['catalog']
            backup.append((courseID, c['title'], c['cred'], c['genED']))

        for c in (obj['major']):
            majList.append(c['title'])

        for c in (obj['minor']):
            minList.append(c['title'])

        courseList = []  # course list
        majorFourList = []  # major four year plan list (return value)
        minorFourList = []  # minor four year plan list (return value)
        minorReqList = []
        sem = "1"  # Keeps track of which semester in database
        total = 0  # Total number of semesters
        ctotal = 0  # Total number of courses in a semester

        courseHist = []  # four year plan list (return value)
        sem = "1"  # Keeps track of which semester in database
        total = 0  # Total number of semesters
        ctotal = 0  # Total number of courses in a semester


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
        policies = []
        for i in range(len(obj['major'])):
            majorFourList.append(self.getFourYear(majList[i]))
            policies.append(self.getPolicies(majList[i]))
        for i in range(len(obj['minor'])):
            minorFourList.append(self.getMinorPlanCourse(minList[i]))
            minorReqList.append(self.getMinorPlanReq(minList[i]))
            policies.append(self.getMinorUnivReq(minList[i]))
            # First array initializer corresponds to which semester you are viewing course for
            # Ex.  fourList[0][1]  =  The first semester and the second course the took that semester

            # All below represnt the second array initializer which corresponds to individual information for a course
            # [0] = The first value indicates which semester the course is for
            # [1] = The subject of the course
            # [2] = The catalog of the course
            # [3] = The title of the course
            # [4] = The number of credits for the course

            # [0, 'ENGL', '103', 'Composition and Research', '4']    Example output for fourList[0][2]

        pub.sendMessage("PPW_information", obj=obj, tcred=cred, courses=courses, numbCourse=numbCourses, major=majList, minor=minList,
                        bcourses=backup, courseHist=courseHist, fourYear=majorFourList, minorFourYear=minorFourList,minorReqList=minorReqList,  policies=policies)
        # pub.sendMessage("FYP_information", obj=obj, courseHist=fourList)

    def getFourYear_refresh(self, majors, minors):
        fouryear = []
        minorfouryear = []
        policies = []
        minorReqList = []

        for m in majors:
            fouryear.append(self.getFourYear(m))
            policies.append(self.getPolicies(m))
        for mi in minors:
            minorfouryear.append(self.getMinorPlanCourse(mi))
            minorReqList.append(self.getMinorPlanReq(mi))
            policies.append(self.getMinorUnivReq(mi))

        pub.sendMessage("FYP_refresh_info", major=majors, minor=minors, FourYear=fouryear, minorFourYear=minorfouryear, minorReqList=minorReqList, policies=policies)

    def getPolicies(self, major):
        myCol = db.get_collection('FourYear')
        i = ""
        obj = myCol.find_one({'major': major})
        if not obj:
            spl = major.split(" ")
            regx = re.compile("^" + spl[0])
            obj1 = myCol.find_one({'major': regx})
            if not obj1:
                print("\n\nNo Major Found\n\n")
            else:
                i = obj1
        else:
            i = obj
        return i['policies']

    def delStud(self, id):
        stud = db["Student"]
        query = {"s_id": int(id)}
        info = stud.delete_many(query)
        if info.deleted_count == 1:
            return "one entry deleted"
        elif info.deleted_count == 0:
            return "no matches found, deleted 0 entries"
        else:
            return str(info.deleted_count) + " entries deleted"

    def delCrs(self, sub, num):
        crs = db["Course"]
        query = {"Subject": sub, "Catalog": Regex(u".*{0}.*".format(num), "i")}
        # this ".*string.*" regex searches for entries containing the given string
        # when searching for a given catalog num normally, the entire string must match
        # a portion of the entries in the db have spaces at the beginning of the catalog num string
        # this regex ignores that space and is true if the field contains the given number anywhere in the string
        info = crs.delete_many(query)
        if info.deleted_count == 1:
            return "one entry deleted"
        elif info.deleted_count == 0:
            return "no matches found, deleted 0 entries"
        else:
            return str(info.deleted_count) + " entries deleted"

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

    def getFourYear(self, major):
        courseList = []  # course list
        fourList = []  # four year plan list (return value)
        sem = "1"  # Keeps track of which semester in database
        total = 0  # Total number of semesters
        ctotal = 0  # Total number of courses in a semester
        i = ""
        myCol = db.get_collection('FourYear')
        obj = myCol.find_one({'major': major})
        if not obj:
            spl = major.split(" ")
            regx = re.compile("^" + spl[0])
            obj1 = myCol.find_one({'major': regx})
            if not obj1:
                print("\n\nNo Major Found\n\n")
            else:
                i = obj1
        else:
            i = obj


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

    def getMinorUnivReq(self, minor):
        reqList = []  # req list
        sem = "1"  # Keeps track of which semester in database
        total = 0  # Total number of semesters
        ctotal = 0  # Total number of courses in a semester

        myCol = db.get_collection('MinPlan')
        i = myCol.find_one({'minor': minor})
        policy = i['university_policies'] + i['minor_req']
        reqList.append(policy)
        return reqList

    def getMinorPlanReq(self, minor):
        reqList = []  # req list
        sem = "1"  # Keeps track of which semester in database
        total = 0  # Total number of semesters
        ctotal = 0  # Total number of courses in a semester

        myCol = db.get_collection('MinPlan')
        i = myCol.find_one({'minor': minor})

        # Gets total number of reqs through error handling
        for j in range(15):  # Max of 15 possible reqs
            stri = "req"  # Append which req to string
            stri = stri + sem
            try:  # Error checks is req is out of range
                (i[stri])  # Sets the total to the currently viewed req
                total = int(sem)
                resl = [j, i[stri]]
                reqList.append(resl)  # Appends that string to a req list
            except KeyError as b:
                total = total  # Last none KeyError semester is stored
            sem = str(int(sem) + 1)
        return reqList

    def getMinorPlanCourse(self, minor):
        courseList = []  # course list
        minList = []  # four year plan list (return value)
        sem = "1"  # Keeps track of which semester in database
        total = 0  # Total number of semesters
        ctotal = 0  # Total number of courses in a semester

        myCol = db.get_collection('MinPlan')
        i = myCol.find_one({'minor': minor})

        # fourList.append(i['policies'])

        # Gets total number of semesters through error handling
        for j in range(15):  # Max of 15 possible semesters needed
            stri = "crs"  # Append which semester to string
            stri = stri + sem
            try:  # Error checks is semester is out of range
                (i[stri])  # Sets the total to the currently viewed semester
                total = int(sem)
            except KeyError as b:
                total = total  # Last none KeyError semester is stored
            sem = str(int(sem) + 1)

        for k in range(total):  # Iterates through each semester from previously calculated value
            stri = "crs"  # Appends which semester to a string
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
            minList.append(courseList)
        return minList

    def insertCSV(self, path):
        myCol = db.get_collection("Crs Test")
        myCol.drop()
        finalOut = []
        myCol = db.get_collection("Crs Test")
        header = ["Course ID", "Eff Date", "Status", "Catalog Descr", "Equiv Crs", "Allowd Unt", "Allow Comp", "Long Title", "Descr", "Offer Nbr", "Acad Group",
                  "Subject", "Catalog", "Acad Org", "CIP Code", "HEGIS Code", "Component", "Equiv Crs", "Course ID", "CRSE ID Descr", "Crse Attr", "CrsAtr Val",
                  "RQ Designation", "RQ Designation Descr", "RQ Designation Formal Descr", "Rq Group", "RQ GRP Descr", "RQ GRP ShortDescr", "Rq Group", "RQ Usage",
                  "RQ Description(Descr80)", "RQ Descr(DESCR254A)", "RQ Descr(Descrlong)", "Grading"]
        with open(path, encoding="utf8") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for each in csv_reader:
                row = {}
                for field in header:
                    row[field] = each[field]
                finalOut.append(row)
        myCol.insert_many(finalOut)

    def openCSV(self):
        path = askopenfilename(
            initialdir="./",
            filetypes=[("CSV File", "*.csv"), ("All Files", ".")],
            title="Choose a Course CSV File")

        if len(path) > 0:
            threading.Thread(target=self.insertCSV(path)).start()



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
