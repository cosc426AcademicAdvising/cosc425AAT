
import pymongo

client = pymongo.MongoClient(
    "mongodb+srv://COSC425AAT:ucciEcY4ItzL6BRN@cluster0.qmhln.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['COSC425AAT']
myCol = db.get_collection('Student')

obj = myCol.find_one({'s_id': 1235123})
stri = "semester_winter"  # Appends which semester to a string
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

for i in range(len(wList)):
    print(wList[i])

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

for i in range(len(sList)):
    print(sList[i])