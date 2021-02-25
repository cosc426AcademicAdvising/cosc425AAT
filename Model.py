from tkinter.filedialog import askopenfilename
import json
from pubsub import pub      # pip install PyPubSub

import pymongo

client = pymongo.MongoClient("mongodb+srv://COSC425AAT:ucciEcY4ItzL6BRN@cluster0.qmhln.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['COSC425AAT']

class Model:
    def __init__(self):
        return

    def listAllMajors(self):
        myCol = db.get_collection('Department')
        obj = myCol.find({'Plan Type': 'MAJ'})
        majors = []
        for i in obj:
            majors.append(i['Descr'])
        return majors

    def listAllMinors(self):
        myCol = db.get_collection('Department')
        obj = myCol.find({'Plan Type': 'MIN'})
        minors = []
        for i in obj:
            minors.append(i['Descr'])
        return minors

    def openJson(self):
        path = askopenfilename(
            initialdir="./",
            filetypes=[("JSON File", "*.json"), ("All Files", ".")],
            title="Choose a Student Schedule file"
        )

        if len(path) > 0:
            print(path)
            with open(path) as f:
                data = json.load(f)
        else:
            return

        student_info = [
            data['student']['name'],
            data['student']['id']
        ]

        for i in student_info:
            print(i)
        pub.sendMessage("PPW_information", arg1=student_info)