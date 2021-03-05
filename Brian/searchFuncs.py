from pymongo import MongoClient
client = MongoClient("mongodb+srv://COSC425AAT:ucciEcY4ItzL6BRN@cluster0.qmhln.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['COSC425AAT']
dept = db["Department"]
stud = db["Student"]
cat = db["Catalog"]

#sub = subject - ex. COSC, MATH, ECON
#num = course number - ex. 320, 362
# returns a list of all courses that match the given subject and gen-ed group
def genEd(sub, grp):
    genList = []
    query = {}
    query["CrsAtr Val"] = grp
    query["Subject"] = sub
    curs = cat.find(query)
    for i in curs:
        genList.append("{0}{1}".format(i["Subject"], i["Catalog"]) + " {0}".format(i["Long Title"]))
    return genList

# returns a list of all gen-ed courses in the given group
def genEdGrp(grp):
    genList = []
    query = {}
    query["CrsAtr Val"] = grp
    curs = cat.find(query)
    for i in curs:
        genList.append("{0}{1}".format(i["Subject"], i["Catalog"]) + " {0}".format(i["Long Title"]))
    return genList

# returns true if the student with the given id has taken the course matching the given subject and number
# false otherwise
def studSrch(sub, num, id):
    # todo: fix numclasses index out of bounds error
    classList = []
    str = sub + " " + num
    numclasses = []
    query = {}
    query["s_id"] = int(id)
    pipeline = [
        {
            "$match": {
                "s_id": int(id)
            }
        },
        {
            u"$project": {
                u"numCourses": {
                    u"$cond": {
                        u"if": {
                            u"$isArray": u"$course_taken"
                        },
                        u"then": {
                            u"$size": u"$course_taken"
                        },
                        u"else": u"err"
                    }
                }
            }
        }
    ]
    curs = stud.find(query)
    cnum = stud.aggregate(
    pipeline,
    allowDiskUse = False
)
    for i in cnum:
        numclasses.append(int('{0}'.format(i['numCourses'])))
    numIter = 0
    for x in curs:
        n = 0
        # print(numclasses[n])
        while (n < numclasses[numIter]):
            if (x["course_taken"][numclasses[numIter] - n]["course_id"] == str):
                return True
            n += 1
        numIter += 1
    return False

# returns a list of all courses with the same requisite group as sub + num
# the first index contains a string of the prerequisites for the courses in the list
def req(sub, num):
    reqList = []
    reqid = 0
    query = {}
    query["Catalog"] = num
    query["Subject"] = sub
    curs = cat.find(query)
    for i in curs:
        reqid = "{0}".format(i["Rq Group"])
        reqList.append("{0}".format(i["RQ Descr(Descrlong)"]))
    q2 = {}
    q2["Rq Group"] = reqid
    curs2 = cat.find(q2)
    for x in curs2:
        reqList.append("{0}{1}".format(x["Subject"], x["Catalog"]) + " {0}".format(x["Long Title"]))
    return reqList

def delStud(id):
    query = {}
    query["s_id"] = int(id)
    info = stud.delete_many(query)
    if (info.deleted_count == 1):
        return "one entry deleted"
    elif (info.deleted_count == 0):
        return "no matches found, deleted 0 entries"
    else:
        return (str(info.deleted_count) + " entries deleted")

#sample input below
mylist = genEd("ART", "3AC")
print(mylist)

mylist2 = genEdGrp("3AC")
print(mylist2)

#not working atm, will fix asap
#studSrch("COSC", "320", "7654321")

mylist3 = req("COSC", " 320")
print(mylist3)

print(delStud(7654321))