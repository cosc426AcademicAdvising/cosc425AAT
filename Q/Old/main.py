import pymongo
import json

client = pymongo.MongoClient("mongodb+srv://COSC425AAT:ucciEcY4ItzL6BRN@cluster0.qmhln.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['COSC425AAT']

# Simply list all objects in whatever collection is passed to it
def listAllObjects(coll):
    obj = coll.find()
    for i in obj:
        print(i)

# List all student info for student collection passed to it
def listAllStudentObjects(coll):
    obj = coll.find()
    for i in obj:
        print(i)

#List all the courses for a student from the student collection
def listStudentsCourses(coll, search):

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
            print(x['First name'], x['Courses'][j]['cred'], x['Courses'][j]['name'], x['Courses'][j]['department'])

        print("\n")     # format

# Search for a course by title from the course collection passed to it
def searchCoursebyTitle(coll, search):
    obj = coll.find({'title': search})
    for i in obj:
        print(i)

# Search for a student by ID from the student collection passed to it
def searchStudentbyId(coll, search):
    obj = coll.find(
        {'Student ID': int(search)}
    )

    # For each object it will print the students first and last name
    for i in obj:
        print(i['First name'], i['Last name'])




###########################################################################################################
####                                        MAIN                                                    #######

# Load file into the database
#with open('planning.json') as f:
#    file_data = json.load(f)
#myCol = db.get_collection('Planning')
#myCol.insert_many(file_data)

# Dispaly welcome message for
print("Welcome to the example Academic Advising Tool Database Interface")
res = input("1. Course Collection\n2. Department Collection\n3. Planning Collection\n4. Student Collection\n5. Generate Planning Form\n")

#case 1 is for the course collection
if int(res) == 1:
    # Assign myCol to the db course collection
    myCol = db.get_collection('Course')

    print("Welcome to the Course Collection\n")

    # Either list all objects or search by title
    choice = input("1. List all objects\n2. Search by course title\n")
    if int(choice) == 1:
        listAllObjects(myCol)
# Case 2 for the department collection
elif int(res) == 2:
    # Assign myCol to the db department collection
    myCol = db.get_collection('Department')
    print("Welcome to the Department Collection\n")

    # Either list all objects or search by a major
    choice = input("1. List all objects\n2. Search by Major\n")
    if int(choice) == 1:
        listAllObjects(myCol)
# Case 3 for the planning collection
elif int(res) == 3:
    # Assign myCol to db planning collection
    myCol = db.get_collection('Planning')
    print("Welcome to the Planning Collection\n")

    # Either list all objects or search by student name
    choice = input("1. List all objects\n2. Search by student name\n")
    if int(choice) == 1:
        listAllObjects(myCol)
# Case 4 for student collection
elif int(res) == 4:
    # Assign myCol to the db student collection
    myCol = db.get_collection('Student')
    print("Welcome to the Student Collection\n")
    # Either list all objects or search by a student ID
    choice = input("1. List all objects\n2. Search by Student ID\n")
    if int(choice) == 1:
        listAllStudentObjects(myCol)
    # After searching by ID the user can display the students name or their courses
    elif int(choice) == 2:
        id = input("Enter the ID you wish to search for\n")
        opt = input("1. View this students name\n2. View only this students courses\n")
        if int(opt) == 1:
            searchStudentbyId(myCol, id)
        elif int(opt) == 2:
            listStudentsCourses(myCol, id)
# Case 5 for Generating program planning form
elif int(res) == 5:
    myCol = db.get_collection('Student')
    aggr = myCol.aggregate([{u"$project": {u"count": {u"$size": u"$Courses"}}}])
    obj = myCol.find()
    for i in aggr:
        y = int(i['count'])
    # iterate through each object in student collection
    for i in obj:
        print("\nStudent Information\n\n",
            i['First name'], "\n", i['Last name'], "\n",
            i['Student ID'], "\n", i['Year'], "\n",
            i['Status'], "\n", i['Major'], "\n",
            i['Minor'], "\n", i['Graduation year'],
            )
        # Iterate through each course in a students courses taken
        print("\nCourses Taken\n")
        for j in range(y):
            print(
                i['Courses'][j]['name'],
                i['Courses'][j]['Semester'],
                i['Courses'][j]['cred'],
                i['Courses'][j]['department']
                )
    # Switch to planning collection
    myCol = db.get_collection('Planning')

    # Determine size of the courses inside the planning collection object
    aggr = myCol.aggregate([{u"$project": {u"count": {u"$size": u"$Courses"}}}])
    obj = myCol.find()
    for i in aggr:
        y = int(i['count'])

    # iterate through each object returned by the cursor
    for i in obj:
        print("\nCourses To Be Taken\n")
        for j in range(y):
            print(
                i['Courses'][j]['name'],
                i['Courses'][j]['semester'],
                i['Courses'][j]['cred'],
                i['Courses'][j]['department']
                )

    #with open("sample.json", "w") as outfile:
    #   json.dump(i, outfile)

