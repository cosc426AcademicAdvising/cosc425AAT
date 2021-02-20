from pymongo import MongoClient

#make sure to change the database/collection names to match your local DB and collections
client = MongoClient('localhost', 27017)
database = client["cosc425"]
collection = database["student"]

sid = input("Enter a student id: ")

query = {}

query["Student ID"] = int(sid)
pipeline = [
    {
        #removes entries that don't have a student id matching sid from the aggregation
            "$match" : {
                "Student ID" : int(sid)
            }
    },
    {
        #projects a new field called numcourses which stores the size of the 'courses' dictionary in the JSON file
        u"$project": {
            u"numCourses": {
                u"$cond": {
                    u"if": {
                        u"$isArray": u"$Courses"
                    },
                    u"then": {
                        u"$size": u"$Courses"
                    },
                    u"else": u"err"
                }
            }
        }
    }
]

cursor = collection.find(query)
courses = collection.aggregate(
    pipeline,
    allowDiskUse = False
)
#used to store the number of courses taken in a semester
courseNumList = []

#appends the result of the aggregation into the courseNumList
for i in courses:
    courseNumList.append(int('{0}'.format(i['numCourses'])))

#prints the department of the first course taken in the given semester, will be changed later for testing
for doc in cursor:
    print(doc['Courses'][0]['department'])

#this line and the next for loop were used for debugging
print(len(courseNumList))

#prints all the entries in courseNumList, more debugging
for x in range(len(courseNumList)):
    print(courseNumList[x])
