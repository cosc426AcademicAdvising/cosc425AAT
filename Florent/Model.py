from tkinter.filedialog import askopenfilename
import json
from pubsub import pub      # pip install PyPubSub


class Model:
    def __init__(self):
        return

    def openSchedule(self):
        path = askopenfilename(
            initialdir="./",
            filetypes=[("JSON File", "*.json"), ("All Files", ".")],
            title="Choose a Student Schedule file"
        )
        if len(path) > 0:
            print(path)
            with open(path) as f:
                data = json.load(f)

        # list of student info
        self.student_info = [
            data['student']['name'],
            str(data['student']['id']),
            str(data['student']['year'])
        ]

        for i in self.student_info:
            print(i)

        pub.sendMessage("student info sent", arg1=self.student_info)