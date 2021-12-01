from json import *

targetFile = 'physicsEng.json'

def wr(data, fname = targetFile):
    with open(fname, 'w') as f:
        dump(data, f, indent = 4)

def append(st,x):
    with open(targetFile) as file:
        d = load(file)
        t = d['semester_{}'.format(x)]
        arr = st.split(',')
        y = {
            "subject": "{0}".format(arr[0].upper()),
            "catalog": "{0}".format(arr[1]),
            "title": "{0}".format(arr[2]),
            "cred": int("{0}".format(arr[3]))
        }
        t.append(y)
    wr(d)


print("enter subject, catalog num, title, and credit hours separated by 1 comma")
print("ENGL,103,Composition and research,4")
print("enter \'next\' to go to the next semester, \'prev\' goes back 1")
x = 1
print("editing semester 1")
while True:
    i = input(">")
    if (i == "done"):
        exit()
    elif (i == "next"):
        x += 1
        print("editing semester {}".format(x))
        continue
    elif (i == "prev"):
        x -= 1
        print("editing semester {}".format(x))
        continue
    else:
        append(i, x)
