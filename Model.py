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
        for c in obj['taking_course']:
            courseID = c['subject'] + " " + c['catalog']
            courses.append((courseID, c['title'], c['cred'], c['genED']))
            cred += c['cred']

        for c in obj['backup_course']:
            courseID = c['subject']+ " " +c['catalog']
            backup.append((courseID, c['title'], c['cred'], c['genED']))

        courseList = []  # course list
        fourList = []  # four year plan list (return value)
        sem = "1"  # Keeps track of which semester in database
        total = 0  # Total number of semesters
        ctotal = 0  # Total number of courses in a semester

        for i in obj['four_year']:

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
                        (obj['four_year'][0][stri][l])
                        ctotal = l + 1  # Sets total number of courses to currently viewed course
                        resl = [k, i[stri][l]['subject'], i[stri][l]['catalog'], i[stri][l]['title'],
                                i[stri][l]['credits']]  # Creates a string value of each objects within array
                        courseList.append(resl)  # Appends that string to a course list
                    except IndexError as c:
                        ctotal = ctotal  # Last none index error course number is stored
                #print(ctotal)
                fourList.append(courseList)  # Appends the course list to the four year plan list

            # First array initializer corresponds to which semester you are viewing course for
            # Ex.  fourList[0][1]  =  The first semester and the second course the took that semester

            # All below represnt the second array initializer which corresponds to individual information for a course
            # [0] = The first value indicates which semester the course is for
            # [1] = The subject of the course
            # [2] = The catalog of the course
            # [3] = The title of the course
            # [4] = The number of credits for the course

            # [0, 'ENGL', '103', 'Composition and Research', '4']    Example output for fourList[0][2]

        pub.sendMessage("PPW_information", obj=obj, tcred=cred, courses=courses, numbCourse=numbCourses, bcourses=backup, courseHist=fourList)

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