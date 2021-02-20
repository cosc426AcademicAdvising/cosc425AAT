import pymongo
import json

#client = pymongo.MongoClient('mongodb://localhost:27017')

client = pymongo.MongoClient("mongodb+srv://COSC425AAT:ucciEcY4ItzL6BRN@cluster0.qmhln.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.COSC425AAT
#db = client['mydbs2']
#db.create_collection('Student')
myCol = db.get_collection('Department')

with open('info.json') as f:
    file_data = json.load(f)

myCol.insert_many(file_data)
'''
query = {'student': {'name': 'John Wick'}}
result = myCol.find(
    query
)

print(result[0])
for i in result:
    print(i[0])
'''