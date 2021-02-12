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
for name in data['student']['name']:
    if data['student']['name'][name]:
        print(data['student']['name'][name])

# id
print(data['student']['id'])

# season
for season in data['student']['season']:
    if data['student']['season'][season]:
        print(season)

# year
print(data['student']['year'])

# major
for major in data['student']['major']:
    print(major)

# minor
for minor in data['student']['minor']:
    print(minor)

# classification
for Cls in data['student']['classification']:
    if data['student']['classification'][Cls]:
        print(Cls)
print()

# course
# in json file 'courses' is an array so we need to
# pass an index in order to access the data
# e.g print(data['courses'][0]['subject'])
for i in range(len(data['courses'])):
    for attr in data['courses'][i]:
        print(data['courses'][i][attr])
    print()
