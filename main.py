from asyncore import read
from hashlib import new
import json
import glob
import os
from traceback import print_tb
class User_register:
    users=[]


    def __init__(self,data):
        
        for d in data:
            added=False
            if len(self.users)==0:
                self.users.append(dict(d))
                added=True
            
            if not added:
                for i  in range(len(self.users)):
                    if self.users[i]['email']==d['email']:
                        dev1=self.users[i]['devices']
                        dev2=d['devices']
                        new_dev=[]
                        for el in dev2:
                            if el not in dev1:
                                new_dev.append(el)
                        if len(new_dev) != 0:
                            self.users[i]['devices'].append(new_dev)
                        added=True 
            if not added:
                self.users.append(dict(d))
                added=True
                    


                       
               


data=[]



files = glob.glob('users/*', recursive=True)
print(files)
for single_file in files:
    print(single_file)
    with open(single_file, 'r') as f:
        studentDict = json.loads(f.read())
        data.append(studentDict)
data1=data[0]
data2=data[1]
data3=data[2]
data4=data[3]
d=(data1)+(data2)+(data3)+(data4)




ur=User_register(d)

print(ur.users)





        

