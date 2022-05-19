from asyncore import read
from hashlib import new
import json
import glob
import os
import re
import ipaddress
from traceback import print_tb





#used for email validation 
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@][a-z0-9]+[\.-]?[a-z0-9]+[.]\w{2,3}$'

"""
Validates emails.
Returns: 
        0 - ok 
        1 - email not valid 
"""
def check(email):
    if (re.search(regex, email)):
        return 0
    else:
        return 1

"""
Validates ip addresses.
Returns: 
        0 - ok 
        1 - ip address not valid 
"""
def validate_ip_address(address):
    try:
        ip = ipaddress.ip_address(address)
        return 0
    except ValueError:
        return 1


class User_register:
    users=[]

    def __init__(self,files):
        result=[]
        for single_file in files:
            with open(single_file, 'r') as f:
                studentDict = json.loads(f.read())
                result.append(studentDict)
        data=[]
        for x in result: data += (x) 
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

   
    def setNameSurname(self, email, name): 
        if isinstance(name,str): 
            for user in self.users:
                if user.get("email")==email: 
                    user.update({"name":name})
            return "No one is associated with " + email 
        else: 
            print("Given argument is not string!")
            
     
    def setIP(self, email, ip): 
        if not isinstance(email,str): 
            print("Given argument is not string!")
            return 
        if validate_ip_address(ip)==1: 
            print("IP is not valid!")
            return 
        for user in self.users:
            if user.get("email")==email: 
                user.update({"ip":ip})
                return 
        print("No IP associated with " + email)

    
    def setDevices(self, email, devices): 
        if isinstance(devices,list):
            valid=True
            for device in devices: 
                if "laptop" not in device and "desktop" not in device and "mobile" not in device: 
                    valid=False
            if not valid: 
                print("Device tags are not valid!")
                return
            for user in self.users:
                if user.get("email")==email: 
                    user.update({"devices":devices})
                    return
            print("No devices associated with " + email)
            return 
        else: 
            print("Device argument is not list!")

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

    def __len__(self):
        return len(self.users)
    
    def __getitem__(self,key):
        for i in range(len(self.users)):
            if(self.users[i]['email']==key):
                u= self.users[i] 
                return u


def getListOfFiles(foldername): 
    files = glob.glob(os.path.join(foldername,'*'), recursive=True)
    print(files)
    return files 


d = getListOfFiles('users')
ur=User_register(d)
print(ur)

print(ur.getNameSurname("bojan.djukic@rt-rk.com"))
print(ur.getDevices("bojan.djukic@rt-rk.com"))
print(ur.getIP("bojn.djukic@rt-rk.com"))

devices =[ "desktop 1", "mobile 2"]
ur.setDevices("bojan.djukic@rt-rk.com",devices)
ur.setIP("bojan.djukic@rt-rk.com","100.100.100.100")
ur.setNameSurname("bojan.djukic@rt-rk.com","xx")

print(ur.getUser("bojan.djukic@rt-rk.com"))

print(len(ur))
print(ur["bojan.djukic@rt-rk.com"])

        

