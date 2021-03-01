import pymongo

client = pymongo.MongoClient("mongodb+srv://COSC425AATRO:ZoCRpw6jHPZ9eYPC@cluster0.qmhln.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['COSC425AAT']

def searchStudentbyID(search):
    myCol = db.get_collection('Student')
    obj = myCol.find({'s_id': int(search)})
    for i in obj:
        print(i)

def searchStudentbyName(search):
    myCol = db.get_collection('Student')
    obj = myCol.find({'name': search})
    for i in obj:
        print(i)

#List all the courses for a student from the student collection
def listStudentsCourses(search):
    coll = db.get_collection('Student')
    # aggregation method to determine the total number of elements in the courses array
    obj = coll.aggregate([{u"$project": {u"count": {u"$size": u"$courses_taken"}}}])

    # Finds all the objects within the courses collection that contain the specified ID
    obj2 = coll.find(
        {'Student ID': int(search)}
    )

    # For loop that goes through each aggregate results and assigns it's array size to Y
    for i in obj:
        y = int(i['count'])

    # Second for loop iterates through each object returned from the courses collection
    for x in obj2:
        # For the range determined by the aggregation it will display all students courses
        for j in range(y):
            print(x['course_taken'][j]['course_id'], x['course_taken'][j]['grade'], x['course_taken'][j]['credits'], x['course_taken'][j]['repeat'])
        print("\n")     # format


# List all the courses for a student from the student collection
def listStudentsPlanningCourses(search):
    coll = db.get_collection('Student')
    # aggregation method to determine the total number of elements in the courses array
    obj = coll.aggregate([{u"$project": {u"count": {u"$size": u"$Courses"}}}])

    # Finds all the objects within the courses collection that contain the specified ID
    obj2 = coll.find(
        {'Student ID': int(search)}
    )

    # For loop that goes through each aggregate results and assigns it's array size to Y
    for i in obj:
        y = int(i['count'])

    # Second for loop iterates through each object returned from the courses collection
    for x in obj2:
        # For the range determined by the aggregation it will display all students courses
        for j in range(y):
            print(x['taking_course'][j]['course_id'])
        print("\n")  #

def listAllMajorsPerDept(search):
    myCol = db.get_collection('Department')
    obj = myCol.find({'Plan Type': 'MAJ'})
    majors = []
    for i in obj:
        if(i['School'] == search):
            majors.append(i['Acad Plan'])
    return majors

def listAllMinorsPerDept(search):
    myCol = db.get_collection('Department')
    obj = myCol.find({'Plan Type': 'MIN'})
    minors = []
    for i in obj:
        if(i['School'] == search):
            minors.append(i['Acad Plan'])
    return minors