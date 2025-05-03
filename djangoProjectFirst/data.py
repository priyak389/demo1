dict1={'studName':'Diya',
       'age':23,
       'isStudent':True,
       'skills':['Programming','Designing','Training'],
       'Address':'Kalyan'
       }

print(dict1)   #This is python native data type data

#convert python native datatype data into json
#dumps(dictionary) --convert python native data type data into json format
#loads(jsonData) -json format convert into python native data type

import json

jsonData=json.dumps(dict1)
print(jsonData)
print(type(jsonData))

dict1=json.loads(jsonData)
print(dict1)
print(type(dict1))

