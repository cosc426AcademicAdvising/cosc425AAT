from pymongo import MongoClient
from bson.regex import Regex

client = MongoClient("mongodb+srv://COSC425AAT:ucciEcY4ItzL6BRN@cluster0.qmhln.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['COSC425AAT']
dept = db["Department"]
stud = db["Student"]
cat = db["Catalog"]
crs = db["Course"]

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
#----------------------------------------------------
# returns a list of all courses with the same requisite group as sub + num
# the first index contains a string of the prerequisites for the courses in the list
def req(sub, num):
    reqList = []
    reqid = 0
    query = {}
    query["Catalog"] = num
    query["Subject"] = sub
    curs = crs.find(query)
    for i in curs:
        reqid = "{0}".format(i["Rq Group"])
        reqList.append("{0}".format(i["RQ Descr(Descrlong)"]))
    q2 = {}
    q2["Rq Group"] = reqid
    curs2 = cat.find(q2)
    for x in curs2:
        reqList.append("{0}{1}".format(x["Subject"], x["Catalog"]) + " {0}".format(x["Long Title"]))
    return reqList

# removes a student entry with a matching ID from the db
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

# some courses have a space in the catalog field, this function selects all courses matching the subject sub and
# contain the number entered in num
# if "cosc 3" is entered, will remove all COSC courses with a number containing 3 anywhere eg. 320, 362, 203, ...
def delCrs(sub, num):
    query = {}
    query["Subject"] = sub
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
# returns a list of strings containing the subject and catalog
# index 0 is course subject eg. COSC, ACCT, etc
# index 1 is the catalog number
# if there are duplicates for whatever reason, all even indexes are subjects and odd indexes are catalog numbers
def getCrs(sub, num):
    query = {}
    query["Subject"] = sub
    query["Catalog"] = Regex(u".*{0}.*".format(num), "i")
    curs = crs.find(query)
    course = []
    for i in curs:
        course.append("{0}".format(i["Subject"]) + "{0}".format(i["Catalog"]))
    return course

def majDeptList(school):
    query = {}
    query["School"] = school
    query["Plan Type"] = { u"$ne": u"Minor" }
    curs = dept.find(query)
    deptList = []
    for i in curs:
        deptList.append("{0}".format(i["Acad Plan"]))
    return deptList

def minDeptList(school):
    query = {}
    query["School"] = school
    query["$and"] = [
        {
            u"Plan Type": {
                u"$ne": u"Major"
            }
        },
        {
            u"Plan Type": {
                u"$ne": u"ROTC"
            }
        }
    ]
    curs = dept.find(query)
    deptList = []
    for i in curs:
        deptList.append("{0}".format(i["Acad Plan"]))
    return deptList

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