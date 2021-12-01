from pymongo import MongoClient
from json import *

def pullStud(id, fname):
    client = MongoClient("mongodb+srv://COSC425AAT:ucciEcY4ItzL6BRN@cluster0.qmhln.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client['COSC425AAT']
    stud = db["Student"]
    query = {"s_id": id}
    curs = stud.find(query)
    data = {}
    for i in curs:
        data["name"] = i['name']
        data["s_id"] = i['s_id']
        data["major"] = i['major']
        data["dept"] = i['dept']
        data['minor'] = i['minor']
        data["status"] = i['status']
        data["year"] = i['year']
        data["credits"] = i['credits']
        data["sem_id"] = i['sem_id']
        data["registering_for"] = i['registering_for']
        data["enrll"] = i['enrll']
        data["advisor_mail"] = i['advisor_mail']
        data["memo"] = i['memo']
        data["course_taken"] = i['course_taken']
        data["taking_course"] = i['taking_course']
        data["backup_course"] = i['backup_course']
        data["four_year"] = i['four_year']
        with open(fname, 'w+') as f:
            dump(data, f, indent=4)


# Sample input
pullStud(1234567, "bob_robert1.json")
