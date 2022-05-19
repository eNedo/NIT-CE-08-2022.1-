from asyncore import read
from hashlib import new
import json
import glob
import os
from traceback import print_tb
import re
import ipaddress
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
                            for device in new_dev: self.users[i]['devices'].append(device)
                            #print("pronadjen duplicirani unos: ",new_dev)
                        added=True 
            if not added:
                self.users.append(dict(d))
                added=True
                
    #TODO check is full name valid 
    def setNameSurname(self, email, name): 
        for user in self.users:
            if user.get("email")==email: 
                user.update({"name":name})
        return "No one is associated with " + email 

    #TODO check is IP valid
    def setIP(self, email, ip): 
        for user in self.users:
            if user.get("email")==email: 
                user.update({"ip":ip})
        return "No IP associated with " + email 

    #TODO maybe check does it contains keywords like desktop,mobile or laptop
    def setDevices(self, email, devices): 
        for user in self.users:
            if user.get("email")==email: 
                user.update({"devices":devices})
        return "No devices associated with " + email 

    def getNameSurname(self,email): 
        for user in self.users:
            if user.get("email")==email: return user.get("name")
        return "No one is associated with  " + email 

    def getDevices(self,email): 
        for user in self.users:
            if user.get("email")==email: return user.get("devices")
        return "No devices associated with " + email 

    def getIP(self,email):
        for user in self.users:
            if user.get("email")==email: return user.get("devices")
        return "No IP associated with " + email 
    
    def getUser(self,email): 
        for user in self.users:
            if user.get("email")==email: return user
        return "No one is associated with  " + email 

    def __str__(self): 
        string=""
        for user in self.users: 
            string = string + str(user) + "\n"
        return string  
            
    def __getitem__(self,key):
        for i in range(len(self.users)):
            if(self.users[i]['email']==key):
                u = self.users[i] 
                return u           


    




    def __len__(self):
        return len(self.users)

    def checkEmail(email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
        if (re.search(regex, email)):
            return 0
        else:
            return 1

    def validate_ip_address(address):
        try:
            ip = ipaddress.ip_address(address)
            return 0
        except ValueError:
            print("IP address {} is not valid".format(address))




def loadUsers(foldername): 
    data=[]
    files = glob.glob(os.path.join(foldername,'*'), recursive=True)
    print(files)
    for single_file in files:
        print(single_file)
        with open(single_file, 'r') as f:
            studentDict = json.loads(f.read())
            data.append(studentDict)
    result=[]
    for x in data: result += (x) 
    return result 


d = loadUsers('users')
ur=User_register(d)
print(ur)
print(len(ur))
print(ur.getNameSurname("bojan.djukic@rt-rk.com"))
print(ur.getDevices("bojan.djukic@rt-rk.com"))
print(ur.getIP("bojn.djukic@rt-rk.com"))

devices =[ "uredjaj1", "uredjaj2"]
ur.setDevices("bojan.djukic@rt-rk.com",devices)
ur.setIP("bojan.djukic@rt-rk.com","1001")
ur.setNameSurname("bojan.djukic@rt-rk.com","xx")

print(ur["bojan.djukic@rt-rk.com"])


print(ur.getUser("bojan.djukic@rt-rk.com"))



        

