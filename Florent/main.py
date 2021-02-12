import json

# open and read json file
infile = open('PPW-myInfo.json', 'r')
infile_data = infile.read()

# parse
data = json.loads(infile_data)

'''
# other method
with open('PPW-myInfo.json') as f:
    data = json.loads(f)
'''

# access like python dictionary
# name
for name in data['Student']['Name']:
    if data['Student']['Name'][name]:
        print(data['Student']['Name'][name])

# id
print(data['Student']['ID Number'])

# season
for season in data['Student']['Season']:
    if data['Student']['Season'][season]:
        print(season)

# year
print(data['Student']['Year'])

# major
for major in data['Student']['Major']:
    print(major)

# minor
for minor in data['Student']['Minor']:
    print(minor)

# classification
for Cls in data['Student']['Classification']:
    if data['Student']['Classification'][Cls]:
        print(Cls)
print()

# courses
# in json file Course is an array so we need to pass
# an index in order to access the data
# e.g print(data['Course'][0]['Subject'])
i = 0
for courses in data['Course']:
    for course in courses:
        print(data['Course'][i][course])
    i += 1
    print()
