import pymongo
client = pymongo.MongoClient(
    "mongodb+srv://COSC425AAT:ucciEcY4ItzL6BRN@cluster0.qmhln.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['COSC425AAT']

myCol = db.get_collection("Department")
query = {"Acad Plan": "ACCTBSAPA"}
res = myCol.delete_one(query)
if res.deleted_count == 1:
    print("good")