from tkinter.filedialog import askopenfilename
import json
import csv
from pubsub import pub  # pip install PyPubSub
import pymongo
from bson.regex import Regex
import re
import threading
import requests
from tkinter import messagebox
from reportlab.pdfgen.canvas import Canvas

#from searchFuncs import stud



token = ""

class Model:
    def __init__(self):
        return

    def setAuthToken(self, tok):
        global token
        token = tok

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

        return name_id

    def getCoursebyRegex(self, sub, cat, title, cred):
        query = {'subject': sub, 'catalog': cat, 'title': title, 'credit': cred}
        response = requests.post("https://cosc426restapi.herokuapp.com/api/Course/Regex",
                                 headers={'auth-token': token}, json=query)
        obj = response.json()
        return obj

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

    def listAllMajorPlan(self):
        response = requests.get("https://cosc426restapi.herokuapp.com/api/Department/MajorPlans", headers={'auth-token': token})
        obj = response.json()
        majors = []
        for i in obj:
            majors.append(i['major'])
        return majors

    def getMinorSchools(self):
        response = requests.get("https://cosc426restapi.herokuapp.com/api/Department/MinorSchool", headers={'auth-token': token})
        return response.json()

    def getMajorSchools(self):
        response = requests.get("https://cosc426restapi.herokuapp.com/api/Department/MajorSchool", headers={'auth-token': token})
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
        courseInfo.append(obj[0]['Subject'])
        courseInfo.append(obj[0]['Catalog'])
        courseInfo.append(obj[0]['Long Title'])
        courseInfo.append(obj[0]['Allowd Unt'])
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
        url = "https://cosc426restapi.herokuapp.com/api/Student/"
        url = url + str(id)
        response = requests.get(url, headers={'auth-token': token})
        data = []
        canvas = Canvas(path, pagesize=(612.0, 792.0))
        try:
            curs = response.json()
            major = ''
            multiMaj = 0
            #for i in curs:
            data.append(curs.get('name'))
            data.append(curs.get('s_id'))
            try:
                data.append('major(s): ' + (curs.get('major')))
                data.append(curs.get('s_id') + ' school')
            except (TypeError, KeyError):
                data.append("Double major")
                multiMaj = 1
            try:
                data.append('minor(s): ' + curs.get('minor'))
            except TypeError:
                data.append("Double minor")
            data.append(curs.get('status'))
            data.append(curs.get('year'))
            data.append('current credits: ' + str(curs.get('credits')))
            data.append(curs.get('sem_id'))
            data.append('Registering for ' + curs.get('registering_for') + ' semester')
            data.append(curs.get('enrll'))
            data.append(curs.get('advisor_mail'))
            major = (curs.get('major'))

            data.append("-----------------------------------------")
            data.append("Current courses:")
            #obj = stud.find_one({'s_id': id})
            for x in curs['taking_course']:
                data.append("       " + x.get('subject') + " " + str(x.get('catalog')) + " " + x.get('title') + " | " + str(
                    x.get('cred')) + ' credits')

            data.append("-----------------------------------------")
            data.append("Backup courses:")
            for x in curs['backup_course']:
                data.append("       " + x.get('subject') + " " + str(x.get('catlog')) + " " + x.get('title') + " | " + str(
                    x.get('cred')) + ' credits')
        except ValueError:
            data.append("JSON value error, possibly an empty schedule?");
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
                except KeyError as b:
                    ctotal = ctotal

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
        url = "https://cosc426restapi.herokuapp.com/api/Student/"
        url = url + str(obj['s_id'])
        response = requests.get(url, headers={'auth-token': token})
        stud = response.json()

        Majtotal = len(stud['major'])

        Mintotal = len(stud['minor'])

        update_url = "https://cosc426restapi.herokuapp.com/api/Update/MajorSet"
        for i in range(len(obj['major'])):
            field1 = 'major.' + str(i) + ".title"
            val = {
                'query': field1,
                's_id': obj['s_id'],
                'maj': obj['major'][i]
            }
            requests.post(update_url, headers={'auth-token': token}, json=val)
        if len(obj['major']) < Majtotal:
            for i in range(len(obj['major']), Majtotal):
                field1 = 'major.' + str(i) + ".title"
                val = {
                    'query': field1,
                    's_id': obj['s_id'],
                    'maj': 'null'
                }
                requests.post(update_url, headers={'auth-token': token}, json=val)

            pull_url = "https://cosc426restapi.herokuapp.com/api/Update/MajorPull"
            for i in range(len(obj['major']), Majtotal):
                val = {
                    's_id': obj['s_id']
                }
                requests.post(pull_url, headers={'auth-token': token}, json=val)

        update_url = "https://cosc426restapi.herokuapp.com/api/Update/MinorSet"
        for i in range(len(obj['minor'])):
            field1 = 'minor.' + str(i) + ".title"
            val = {
                'query': field1,
                's_id': obj['s_id'],
                'min': obj['minor'][i]
            }
            requests.post(update_url, headers={'auth-token': token}, json=val)

        for i in range(len(obj['minor']), Mintotal):
            field1 = 'minor.' + str(i) + ".title"
            val = {
                'query': field1,
                's_id': obj['s_id'],
                'min': 'null'
            }
            requests.post(update_url, headers={'auth-token': token}, json=val)

        pull_url = "https://cosc426restapi.herokuapp.com/api/Update/MinorPull"

        for i in range(len(obj['minor']), Mintotal):
            val = {
                's_id': obj['s_id']
            }
            requests.post(pull_url, headers={'auth-token': token}, json=val)


        # Original total number of course student plans to take
        CTtotal = len(stud['taking_course'])

        # Original total number of courses student has for backups
        BUtotal = len(stud['backup_course'])

        update_url = "https://cosc426restapi.herokuapp.com/api/Update/CourseSet"

        print(len(obj['taking_course']))

        # Iterate through each course a student plans to take and update the fields in the database
        for i in range(len(obj['taking_course'])):

            subcat = obj['taking_course'][i][0].split()
            print(subcat[0])
            print(subcat[1])
            field1 = "taking_course." + str(i) + ".subject"
            field2 = "taking_course." + str(i) + ".catalog"
            field3 = "taking_course." + str(i) + ".title"
            field4 = "taking_course." + str(i) + ".cred"
            field5 = "taking_course." + str(i) + ".genED"
            val = {
                'field1': field1,
                'field2': field2,
                'field3': field3,
                'field4': field4,
                'field5': field5,
                'sub': subcat[0],
                'cat': subcat[1],
                'title': obj['taking_course'][i][1],
                'cred': obj['taking_course'][i][2],
                'gen': obj['taking_course'][i][3],
                's_id': obj['s_id']
            }
            requests.post(update_url, headers={'auth-token': token}, json=val)

        reset_url = "https://cosc426restapi.herokuapp.com/api/Update/CourseReset"

        # Iterate through remaining courses and assign null value to subject indicating their need for removal
        for i in range(len(obj['taking_course']), CTtotal):
            field1 = "taking_course." + str(i) + ".subject"
            val = {
                'field1': field1,
                's_id': obj['s_id']
            }
            requests.post(reset_url, headers={'auth-token': token}, json=val)

        pull_url = "https://cosc426restapi.herokuapp.com/api/Update/CoursePull"

        # Iterate again through remaining courses and pull those courses from database that are no longer needed
        for i in range(len(obj['taking_course']), CTtotal):
            val = {
                's_id': obj['s_id']
            }
            requests.post(pull_url, headers={'auth-token': token}, json=val)

        # Iterate through each backup course and update the fields in the database
        for i in range(len(obj['backup_course'])):
            subcat = obj['backup_course'][i][0].split()
            field1 = "backup_course." + str(i) + ".subject"
            field2 = "backup_course." + str(i) + ".catalog"
            field3 = "backup_course." + str(i) + ".title"
            field4 = "backup_course." + str(i) + ".cred"
            field5 = "backup_course." + str(i) + ".genED"
            val = {
                'field1': field1,
                'field2': field2,
                'field3': field3,
                'field4': field4,
                'field5': field5,
                'sub': subcat[0],
                'cat': subcat[1],
                'title': obj['backup_course'][i][1],
                'cred': obj['backup_course'][i][2],
                'gen': obj['backup_course'][i][3],
                's_id': obj['s_id']
            }
            requests.post(update_url, headers={'auth-token': token}, json=val)

        # Iterate through remaining courses and assign null value to subject indicating their need for removal
        for i in range(len(obj['backup_course']), BUtotal):
            print("A__")
            field1 = "backup_course." + str(i) + ".subject"
            val = {
                'field1': field1,
                's_id': obj['s_id']
            }
            requests.post(reset_url, headers={'auth-token': token}, json=val)

        pull_url = "https://cosc426restapi.herokuapp.com/api/Update/BackCoursePull"

        # Iterate again through remaining courses and pull those courses from database that are no longer needed
        for i in range(len(obj['backup_course']), BUtotal):
            val = {
                's_id': obj['s_id']
            }
            requests.post(pull_url, headers={'auth-token': token}, json=val)

        messagebox.showinfo("Save", "Student's data successfully saved!")

    def updateMajPlan(self, obj):
        url = "https://cosc426restapi.herokuapp.com/api/Update/MajorPlan"
        requests.post(url, headers={'auth-token': token}, json=obj)
        messagebox.showinfo("Save", "Major's data successfully saved!")

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
