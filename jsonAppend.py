from json import *

targetFile = 'muscInst.json'

def wr(data, fname = targetFile):
    with open(fname, 'w') as f:
        dump(data, f, indent = 4)

def append(st):
    with open(targetFile) as file:
        d=load(file)
        t = d['four_year']
        arr = st.split(',')
        y = {
            "semester": "Year {0} Semester {1}".format(arr[0], arr[1]),
            "subject": "{0}".format(arr[2]),
            "catalog": "{0}".format(arr[3]),
            "title": "{0}".format(arr[4]),
            "cred": int("{0}".format(arr[5]))
        }
        t.append(y)
    wr(d)


print("enter year, semester number, subject, catalog num, title, and credit hours separated by 1 comma")
print("ex 1,1,ENGL,103,Composition and research, 4")
while True:
    i = input(">")
    append(i)

