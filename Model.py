from tkinter.filedialog import askopenfilename
import json
import logger
import csv
from pubsub import pub  # pip install PyPubSub
import pymongo
from bson.regex import Regex
import re
import threading
import requests
from tkinter import messagebox
# from reportlab.pdfgen.canvas import Canvas

client = pymongo.MongoClient(
    "mongodb+srv://COSC425AAT:ucciEcY4ItzL6BRN@cluster0.qmhln.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)
db = client['COSC425AAT']

token = 'v2.public.eyJ1cm46ZXhhbXBsZTpjbGFpbSI6IkRCIEFjY2VzcyIsImlhdCI6IjIwMjEtMDktMTZUMDE6MTQ6MTkuNzg0WiJ97RHPZW4HrIIBSO8QkD9fT58OCbI29IMCq5bWOPW3VZFf5kAnu4ndpuNedfZ5fS388xx1UHE6Tf29RjxiTVd_Aw'

class Model:
    def __init__(self):
        return

    def getAllStudents(self):
        stud = db["Student"]
        name_id = {}
        obj = stud.aggregate([
            {
                # Groups all unique name and id combinations in the student collection
                "$group": {
                    "_id": {
                        "s_id": "$s_id",
                        "name": "$name"
                    }
                }
            },
            {
                # Projects each of those unique values into a list to be assigned to 'obj'
                "$project": {
                    "_id": 0,
                    "s_id": "$_id.s_id",
                    "name": "$_id.name"
                }
            }
        ])

        # Loops through each value in the object and assigns them to a 2D list
        j = 0
        for i in obj:
            name_id[j] = i
            j = j + 1

        # Example print statement
        #print(name_id[3]["name"], name_id[3]["s_id"])
        #print(name_id[5]["s_id"])

        return name_id


    def getAllStudentIds(self):
        id = []
        myCol = db.get_collection("Student")
        id = myCol.distinct('s_id')
        return id

    def listAllMajors(self):
        response = requests.get("https://cosc426restapi.herokuapp.com/api/Department/Major", headers={'auth-token': token})
        obj = response.json()
        majors = []
        for i in obj:
            majors.append(i['Acad Plan'])
        return majors

    def listAllMinors(self):
        response = requests.get("https://cosc426restapi.herokuapp.com/api/Department/Minor", headers={'auth-token': token})
        obj = response.json()
        minors = []
        for i in obj:
            minors.append(i['Acad Plan'])
        return minors

    def getSchools(self):
        response = requests.get("https://cosc426restapi.herokuapp.com/api/Department/School", headers={'auth-token': token})
        return response.json()

    def getMajorsbySchool(self, schools):
        majList = []
        url = "https://cosc426restapi.herokuapp.com/api/Department/Major/"
        url = url + schools
        response = requests.get(url, headers={'auth-token': token})
        obj = response.json()
        for i in obj:
            majList.append(i['Acad Plan'])
        return majList

    def getMinorsbySchool(self, schools):
        minList = []
        url = "https://cosc426restapi.herokuapp.com/api/Department/Minor/"
        url = url + schools
        response = requests.get(url, headers={'auth-token': token})
        obj = response.json()
        for i in obj:
            minList.append(i['Acad Plan'])
        return minList

    # Get a course by searching for subject and catalog
    def getCoursebySubCat(self, sub, cat):
        url = "https://cosc426restapi.herokuapp.com/api/Course/"
        url = url + sub + "/"
        url = url + cat
        response = requests.get(url, headers={'auth-token': token})
        obj = response.json()
        courseInfo = []
        courseInfo.append(obj['Subject'])
        courseInfo.append(obj['Catalog'])
        courseInfo.append(obj['Long Title'])
        courseInfo.append(obj['Allowd Unt'])
        return courseInfo

    # Displays what prereqs are necessary for a subject + catalog
    def getPreReq(self, subject, catalog):
        url = "https://cosc426restapi.herokuapp.com/api/Course/"
        url = url + subject + "/"
        url = url + catalog
        response = requests.get(url, headers={'auth-token': token})
        obj = response.json()
        print(obj['RQ Descr(Descrlong)'])
        return obj

    def getSubjects(self):
        url = "https://cosc426restapi.herokuapp.com/api/Course/Subject/"
        response = requests.get(url, headers={'auth-token': token})
        obj = response.json()
        return obj

    def mkPdf(self, id, path):
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
                data.append('major(s): ' + str(i['major']))
                data.append(i['dept'] + ' school')
            except (TypeError, KeyError):
                data.append("Double major")
                multiMaj = 1
            try:
                data.append('minor(s): ' + str(i['minor']))
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

        x = 72
        y = 725
        for z in range(len(data)):
            canvas.drawString(x, y, str(data[z]))
            y -= 20
            if (y <= 75):
                canvas.showPage()
                y = 725

        canvas.save()

    def pullStud(self, id, fname):
        url = "https://cosc426restapi.herokuapp.com/api/Student/"
        url = url + str(id)
        response = requests.get(url, headers={'auth-token': token})
        obj = response.json()
        data = {}
        for i in obj:
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
        url = "https://cosc426restapi.herokuapp.com/api/Student/"
        url = url + str(sid)
        response = requests.get(url, headers={'auth-token': token})
        obj = response.json()
        numbCourses = 0
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

        stri = "semester_winter"
        wList = []
        for l in range(8):
            try:
                (obj['course_taken'][0][stri][l])
                resl = [obj['course_taken'][0][stri][l]['subject'], obj['course_taken'][0][stri][l]['catalog'],
                        obj['course_taken'][0][stri][l]['title'],
                        obj['course_taken'][0][stri][l]['credits'], obj['course_taken'][0][stri][l]['grade']]
                wList.append(resl)
            except IndexError as b:
                continue
            except KeyError as c:
                continue

        stri = "semester_summer"
        sList = []
        for l in range(8):
            try:
                (obj['course_taken'][0][stri][l])
                resl = [obj['course_taken'][0][stri][l]['subject'], obj['course_taken'][0][stri][l]['catalog'],
                        obj['course_taken'][0][stri][l]['title'],
                        obj['course_taken'][0][stri][l]['credits'], obj['course_taken'][0][stri][l]['grade']]
                sList.append(resl)
            except IndexError as b:
                continue
            except KeyError as c:
                continue

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
                        bcourses=backup, courseHist=courseHist, fourYear=majorFourList, minorFourYear=minorFourList,minorReqList=minorReqList,  policies=policies,
                        sumCourse=sList, winCourse=wList)
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
        url = "https://cosc426restapi.herokuapp.com/api/FourYear/Policy/"
        url = url + major
        response = requests.get(url, headers={'auth-token': token})
        return response.json()

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

    def addMajor(self, major, program, school, FullSchool):
        url = "https://cosc426restapi.herokuapp.com/api/Department/Major/Add"
        check_url = "https://cosc426restapi.herokuapp.com/api/Department/MajorIn/"
        check_url = check_url + major
        check_response = requests.get(check_url)
        if(check_response.json() == 0):
            val = {'Acad_Plan': major, 'Plan_Type': 'Major', 'Acad_Prog': program, 'School': school, 'School_Full_Name': FullSchool}
            response = requests.post(url, headers={'auth-token': token}, json=val)
            obj = response.json()
        else:
            print("Already in")



    def addMinor(self, minor, program, school, FullSchool):
        url = "https://cosc426restapi.herokuapp.com/api/Department/Minor/Add"
        check_url = "https://cosc426restapi.herokuapp.com/api/Department/MinorIn/"
        check_url = check_url + minor
        check_response = requests.get(check_url)
        if (check_response.json() == 0):
            val = {'Acad_Plan': minor, 'Plan_Type': 'Minor', 'Acad_Prog': program, 'School': school,
                   'School_Full_Name': FullSchool}
            response = requests.post(url, headers={'auth-token': token}, json=val)
            obj = response.json()
        else:
            print("Already in")

    def delMajor(self, acad):
        major = acad
        url = "https://cosc426restapi.herokuapp.com/api/Department/Major/Delete/"
        url = url + major
        check_url = "https://cosc426restapi.herokuapp.com/api/Department/MajorIn/"
        check_url = check_url + major
        check_response = requests.get(check_url)
        if (check_response.json() == 1):
            response = requests.post(url, headers={'auth-token': token})
            obj = response.json()
        else:
            print("Not Already in")

    def delMinor(self, acad):
        minor = acad
        url = "https://cosc426restapi.herokuapp.com/api/Department/Minor/Delete/"
        url = url + minor
        check_url = "https://cosc426restapi.herokuapp.com/api/Department/MinorIn/"
        check_url = check_url + minor
        check_response = requests.get(check_url)
        if (check_response.json() == 1):
            response = requests.post(url, headers={'auth-token': token})
            obj = response.json()
        else:
            print("Not Already in")

    def getFourYearJson(self, maj):
        url = "https://cosc426restapi.herokuapp.com/api/FourYear/MajorPlan/ARTBA"
        print(maj)
        url_temp = url + maj
        response = requests.get(url, headers={'auth-token': token})
        obj = response.json()
        print(response.json())


    def getFourYear(self, major):
        courseList = []  # course list
        fourList = []  # four year plan list (return value)
        sem = "1"  # Keeps track of which semester in database
        total = 0  # Total number of semesters
        ctotal = 0  # Total number of courses in a semester
        i = ""

        check_url = "https://cosc426restapi.herokuapp.com/api/FourYear/FourYearIn/"
        check_url = check_url + major

        url = "https://cosc426restapi.herokuapp.com/api/FourYear/MajorPlan/"
        url_temp = url + major

        response = requests.get(check_url, headers={'auth-token': token})

        if response.json() == 1:
            response = requests.get(url_temp, headers={'auth-token': token})
            obj = response.json()
            i = obj
        else:
            check_url = "https://cosc426restapi.herokuapp.com/api/FourYear/FourYearInRegex/"
            spl = major.split(" ")
            regx = "^" + spl[0]
            check_url = check_url + regx
            response = requests.get(check_url, headers={'auth-token': token})
            if response.json() == 1:
                url_alt = url + "Regex/" + regx
                response = requests.get(url_alt, headers={'auth-token': token})
                obj1 = response.json()
                i = obj1
            else:
                i = ""
                # No four year plan exists for major

    

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
                            i[stri][l]['cred']]  # Creates a string value of each objects within array
                    courseList.append(resl)  # Appends that string to a course list
                except IndexError as c:
                    ctotal = ctotal  # Last none index error course number is stored
            # print(ctotal)
            fourList.append(courseList)
        return fourList

    def getMinorUnivReq(self, minor):
        reqList = []
        url = "https://cosc426restapi.herokuapp.com/api/MinPlan/Plan/"
        url = url + minor
        response = requests.get(url, headers={'auth-token': token})
        obj = response.json()
        policy = obj['minor_req']
        reqList.append(policy)
        return reqList

    def getMinorPlanReq(self, minor):
        reqList = []  # req list
        sem = "1"  # Keeps track of which semester in database
        total = 0  # Total number of semesters
        ctotal = 0  # Total number of courses in a semester

        url = "https://cosc426restapi.herokuapp.com/api/MinPlan/Plan/"
        url = url + minor
        response = requests.get(url, headers={'auth-token': token})
        i = response.json()
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

        url = "https://cosc426restapi.herokuapp.com/api/MinPlan/Plan/"
        url = url + minor
        response = requests.get(url, headers={'auth-token': token})
        i = response.json()
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

    def updateStudent(self, obj):
        myCol = db.get_collection('Student')
        stud = myCol.find_one({'s_id': int(obj['s_id'])})

        Majtotal = len(stud['major'])

        Mintotal = len(stud['minor'])

        for i in range(len(obj['major'])):
            field1 = 'major.' + str(i) + ".title"
            field2 = 'major.' + str(i) + '.school'
            myCol.update_one({'s_id': int(obj['s_id'])},
                             {'$set': {
                                 field1: obj['major'][i],
                                 field2: ""
                             }})

        for i in range(len(obj['major']), Majtotal):
            field1 = 'major.' + str(i) + ".title"
            field2 = 'major.' + str(i) + '.school'
            myCol.update_one({'s_id': int(obj['s_id'])},
                             {'$set': {
                                 field1: 'null',
                                 field2: ""
                             }})

        for i in range(len(obj['major']), Majtotal):
            field1 = 'major.' + str(i) + ".title"
            myCol.update_one({'s_id': int(obj['s_id'])},
                             {'$pull': {
                                 'major': {'title': 'null'}
                             }})

        for i in range(len(obj['minor'])):
            field1 = 'minor.' + str(i) + ".title"
            field2 = 'minor.' + str(i) + '.school'
            myCol.update_one({'s_id': int(obj['s_id'])},
                             {'$set': {
                                 field1: obj['minor'][i],
                                 field2: ""
                             }})

        for i in range(len(obj['minor']), Mintotal):
            field1 = 'minor.' + str(i) + ".title"
            field2 = 'minor.' + str(i) + '.school'
            myCol.update_one({'s_id': int(obj['s_id'])},
                             {'$set': {
                                 field1: 'null',
                                 field2: ""
                             }})

        for i in range(len(obj['minor']), Mintotal):
            field1 = 'minor.' + str(i) + ".title"
            myCol.update_one({'s_id': int(obj['s_id'])},
                             {'$pull': {
                                 'minor': {'title': 'null'}
                             }})

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
        messagebox.showinfo("Save", "Student's data successfully saved!")

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
