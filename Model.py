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

token = ""

class Model:
    def __init__(self):
        return

    # Initialize paseto token for API access
    def setAuthToken(self, tok):
        global token
        token = tok

    # Requests a list of all students in database from the api
    def getAllStudents(self):
        name_id = {}
        response = requests.get("https://cosc426restapi.herokuapp.com/api/Student/all/students",
                                headers={'auth-token': token})
        obj = response.json()

        # Loops through each value in the object and assigns them to a 2D list
        j = 0
        for i in obj:
            name_id[j] = i
            j = j + 1

        return name_id

    # Requests a list of all Courses that match the specified fields
    def getCoursebyRegex(self, sub, cat, title, cred):
        # Place fields in an object to be packed in body of request
        query = {'subject': sub, 'catalog': cat, 'title': title, 'credit': cred}
        # Make a post request to the API through route /api/Course/Regex
        # Specify the paseto token in the 'auth-token' header
        # json=query is packing the object in the body of the request with a format of json
        response = requests.post("https://cosc426restapi.herokuapp.com/api/Course/Regex",
                                 headers={'auth-token': token}, json=query)
        # List of courses is the returned value if successful
        # Convert returned values into json
        obj = response.json()
        return obj

    # Returns a list of all student ID's
    def getAllStudentIds(self):
        response = requests.get("https://cosc426restapi.herokuapp.com/api/Student/all/studentsIds",
                                headers={'auth-token': token})
        id = response.json()
        return id

    # Requests a list of all majors in database
    def listAllMajors(self):
        response = requests.get("https://cosc426restapi.herokuapp.com/api/Department/Major", headers={'auth-token': token})
        obj = response.json()
        majors = []
        for i in obj:
            majors.append(i['Acad Plan'])
        return majors

    # Requests a list of all minors in dataabase
    def listAllMinors(self):
        response = requests.get("https://cosc426restapi.herokuapp.com/api/Department/Minor", headers={'auth-token': token})
        obj = response.json()
        minors = []
        for i in obj:
            minors.append(i['Acad Plan'])
        return minors

    # Requests a list of all majors with Four Year plans
    def listAllMajorPlan(self):
        response = requests.get("https://cosc426restapi.herokuapp.com/api/Department/MajorPlans", headers={'auth-token': token})
        obj = response.json()
        majors = []
        for i in obj:
            majors.append(i['major'])
        return majors

    # Requests a list of all minors with Four Year plans
    def listAllMinorPlan(self):
        response = requests.get("https://cosc426restapi.herokuapp.com/api/Department/MinorPlans",
                                headers={'auth-token': token})
        obj = response.json()
        minors = []
        for i in obj:
            minors.append(i['minor'])
        return minors

    # Requests a list of all schools under a specified minor
    def getMinorSchools(self):
        response = requests.get("https://cosc426restapi.herokuapp.com/api/Department/MinorSchool", headers={'auth-token': token})
        return response.json()

    # Requests a list all schools under a specified major
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

    # Requests a list of all unique subjects
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
                data.append("       " + x.get('subject') + " " + str(x.get('catalog')) + " " + x.get('title') + " | " + str(
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

    # Requests a student with specified id and name
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

    # Requests a student with specified id and name
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
            try:
                minorFourList.append(self.getMinorPlanCourse(minList[i]))
                minorReqList.append(self.getMinorPlanReq(minList[i]))
                policies.append(self.getMinorUnivReq(minList[i]))
            except ValueError:
                print("json decode failed")
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

    # Requests a list of all policies within a Four Year plan for a specified major
    def getPolicies(self, major):
        url = "https://cosc426restapi.herokuapp.com/api/FourYear/Policy/"
        url = url + major
        response = requests.get(url, headers={'auth-token': token})
        return response.json()

    # Requests to add a new major to the database
    # Needs the major abbrev, program/title, school name (short), and school name (long)
    def addMajor(self, major, program, school, FullSchool):
        url = "https://cosc426restapi.herokuapp.com/api/Department/Major/Add"
        check_url = "https://cosc426restapi.herokuapp.com/api/Department/MajorIn/"
        check_url = check_url + major
        check_response = requests.get(check_url)
        # First checks to see if major already exists, if not then proceed with insert
        if(check_response.json() == 0):
            val = {'Acad_Plan': major, 'Plan_Type': 'Major', 'Acad_Prog': program, 'School': school, 'School_Full_Name': FullSchool}
            response = requests.post(url, headers={'auth-token': token}, json=val)
            obj = response.json()
        else:
            print("Already in")


    # Requests to add a new minor to the database
    # Needs the minor abbrev, program/title, school name (short), and school name (long)
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

    # Requests to remove a major from the database by the specified major abbrev
    def delMajor(self, acad):
        major = acad
        url = "https://cosc426restapi.herokuapp.com/api/Department/Major/Delete/"
        url = url + major
        check_url = "https://cosc426restapi.herokuapp.com/api/Department/MajorIn/"
        check_url = check_url + major
        check_response = requests.get(check_url, headers={'auth-token': token})
        # First checks if major exists, if so proceed with delete

        if (check_response.json() == 1):
            response = requests.post(url, headers={'auth-token': token})
            obj = response.json()
        else:
            print("Not Already in")

    # Requests to remove a minor from the database with the specified minor abbrev
    def delMinor(self, acad):
        minor = acad
        url = "https://cosc426restapi.herokuapp.com/api/Department/Minor/Delete/"
        url = url + minor
        check_url = "https://cosc426restapi.herokuapp.com/api/Department/MinorIn/"
        check_url = check_url + minor
        check_response = requests.get(check_url, headers={'auth-token': token})
        if (check_response.json() == 1):
            response = requests.post(url, headers={'auth-token': token})
            obj = response.json()
        else:
            print("Not Already in")

    # Requests a Four Year plan by the specified major abbrev
    def getFourYearJson(self, maj):
        url = "https://cosc426restapi.herokuapp.com/api/FourYear/MajorPlan/ARTBA"
        url_temp = url + maj
        response = requests.get(url, headers={'auth-token': token})
        obj = response.json()

    # Requests a Four Year plan by the specified major abbrev
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

        # First checks if major already exists in database,

        if response.json() == 1:
            response = requests.get(url_temp, headers={'auth-token': token})
            obj = response.json()
            i = obj
        # if not then perform a regex search to find one that is closely associated
        else:
            check_url = "https://cosc426restapi.herokuapp.com/api/FourYear/FourYearInRegex/"
            spl = major.split(" ")
            regx = "^" + spl[0]
            check_url = check_url + regx
            response = requests.get(check_url, headers={'auth-token': token})
            # Checks again that a plan could be found through regex search
            if response.json() == 1:
                url_alt = url + "Regex/" + regx
                response = requests.get(url_alt, headers={'auth-token': token})
                obj1 = response.json()
                i = obj1
            # If not then no plan exists for that major
            else:
                i = ""
        if(i != ""):
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

    # Requests the university requirements from a minor plan for a specified minor
    def getMinorUnivReq(self, minor):
        reqList = []
        url = "https://cosc426restapi.herokuapp.com/api/MinPlan/Plan/"
        url = url + minor
        response = requests.get(url, headers={'auth-token': token})
        obj = response.json()
        policy = obj['minor_req']
        reqList.append(policy)
        return reqList

    # Requests the course group requirements for a minor plan for a specified minor
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

    # Requests the courses in a minor plan for a specified minor
    def getMinorPlanCourse(self, minor):
        courseList = []  # course list
        minList = []  # four year plan list (return value)
        sem = "1"  # Keeps track of which semester in database
        total = 0  # Total number of semesters
        ctotal = 0  # Total number of courses in a semester

        url = "https://cosc426restapi.herokuapp.com/api/MinPlan/Plan/"
        url = url + minor
        print(minor)
        response = requests.get(url, headers={'auth-token': token})
        i = response.json()
        print(i)
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
            for l in range(15):  # Max of 15 possible courses recommended during any given semester

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

    # Updates student information whenever user requests to save a student
    def updateStudent(self, obj):
        #print(obj)
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
            #print(obj)
            #print(subcat[0])
            #print(subcat[1])
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

    # Requests to post an update to a four year plan for a specified major
    # Object contains all the course information for a Four Year plan
    def updateMajPlan(self, obj):
        url = "https://cosc426restapi.herokuapp.com/api/Update/MajorPlan"
        requests.post(url, headers={'auth-token': token}, json=obj)
        messagebox.showinfo("Save", "Major's data successfully saved!")

    # Requests to post an update to a Minor track plan for a specified minor
    # Object contains all the course information for each course group
    # Req contains all the requirement information for each of the course groups
    def updateMinPlan(self, obj):
        url = "https://cosc426restapi.herokuapp.com/api/Update/MinorPlan"
        requests.post(url, headers={'auth-token': token}, json=obj)
        messagebox.showinfo("Save", "Major's data successfully saved!")

    # Update the course database collection through a file upload
    # Accepts csv files from excel and must follow the header specified below
    # Should occur once a semester to refresh the courses that will be offered in the upcoming semester
    def insertCSV(self, path):
        finalOut = []
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

        # url = "http://localhost:5000/api/Course/insertCSV"
        # requests.post(url, headers={'auth-token': token}, json=finalOut)

    # Function to open a csv file, used to insert CSV
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
