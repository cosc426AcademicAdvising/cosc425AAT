import pymongo
import json

client = pymongo.MongoClient('mongodb://localhost:27017')

db = client['mydbs']
# db.create_collection('Department')
myCol = db.get_collection('Major')

with open('info3.json') as f:
    file_data = json.load(f)

data = [
    {
        'title': 'Computer Science',
        'abbrev': 'COSC',
        'Department': 'Henson'
    },
    {
        'title': 'Mathematics',
        'abbrev': 'Math',
        'Department': 'Henson'
    },
    {
        'title': 'Physics',
        'abbrev': 'PHYS',
        'Department': 'Henson'
    },
    {
        'title': 'Chemistry',
        'abbrev': 'CHEM',
        'Department': 'Henson'
    },
    {
        'title': 'Economics',
        'abbrev': 'ECON',
        'Department': 'Perdue'
    },
    {
        'title': 'Finance',
        'abbrev': 'FINN',
        'Department': 'Perdue'
    },
    {
        'title': 'Music Recording',
        'abbrev': 'MUSR',
        'Department': 'Fulton'
    },
    {
        'title': 'Music Production',
        'abbrev': 'MUSP',
        'Department': 'Fulton'
    }

]

myCol.insert_many(file_data)

result = myCol.find({
        'Department': 'Henson'
})

for i in result:
    print(i["title"], i["abbrev"], i["Department"])
