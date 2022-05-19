from asyncore import read
from hashlib import new
import json
import glob
import os
import re
import ipaddress
from traceback import print_tb


class User_register():
    users=[]
    def __init__(self,files):
        self.files = files
        datasum = []
        for single_file in files:
            with open(single_file, 'r') as f:
                studentDict = json.loads(f.read())
                datasum.append(studentDict)

        listObj = []
        #users = []
        fsum=open('sumfile.json', 'w')
        for data in datasum:
            for i in range(len(data)):
                if validate_ip_address(data[i]['ip']) != 0:
                    print(f"Bad ip address {data[i]['ip']}!!!")
                else:
                    if check(data[i]['email']) != 0:
                        print(f"Bad email address {data[i]['email']}!!!")
                    else:
                        listObj.append(data[i])
        for d in listObj:
            added = False
            if len(self.users) == 0:
                self.users.append(dict(d))
                added = True

            if not added:
                for i in range(len(self.users)):
                    if self.users[i]['email'] == d['email']:
                        dev1 = self.users[i]['devices']
                        dev2 = d['devices']
                        new_dev = []
                        for el in dev2:
                            if el not in dev1:
                                new_dev.append(el)
                        if len(new_dev) != 0:
                            self.users[i]['devices'].append(new_dev)
                        added = True
            if not added:
                self.users.append(dict(d))
                added = True
        json_object = json.dumps(self.users, indent=4)
        fsum.write(json_object)
        fsum.close()
        #print(listObj)

   

   
    def setNameSurname(self, email, name): 
        if isinstance(name,str): 
            if  not self.checkEmail(email):   return 
            for user in self.users:
                if user.get("email")==email: 
                    user.update({"name":name})
                    return 
            "No one is associated with " + email 
        else: 
            print("Given argument is not string!")
            
     
    def setIP(self, email, ip): 
        if not isinstance(email,str): 
            print("Given argument is not string!")
            return 
        if not self.checkEmail(email): return 
        if not self.validate_ip_address(ip): return 
        for user in self.users:
            if user.get("email")==email: 
                user.update({"ip":ip})
                return 
        print("No IP associated with " + email)

    
    def setDevices(self, email, devices): 
        if isinstance(devices,list):
            valid=True
            if not self.checkEmail(email):    return 
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
            
  
    #Validates ip addresses.
    def validate_ip_address(self,address):
        try:
            ip = ipaddress.ip_address(address)
            return True
        except ValueError:
             print("IP address {} is not valid".format(address))
             return False

    #Validates emails.
    def checkEmail(self,email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
        if (re.search(regex, email)):
            print("Email is not valid")
            return False
        else:
            return True

    def __len__(self):
        return len(self.users)
    
    def __getitem__(self,key):
        for i in range(len(self.users)):
            if(self.users[i]['email']==key):
               return self.users[i] 
               
    def __setitem__(self,key,value): 
        if isinstance(key,str): 
            if not self.checkEmail(key): return 
        else: 
            print("key is not string")
            return 
        if isinstance(value,list): 
            self.setDevices(key,value) 
        elif isinstance(value,str): 
            try:
                socket.inet_aton(value)
                self.setIP(key,value) 
            except socket.error:
              self.setNameSurname(key,value) 
        else: 
            print("rvalue is not valid")

def getListOfFiles(foldername): 
    files = glob.glob(os.path.join(foldername,'*'), recursive=True)
    print(files)
    return files 


d = getListOfFiles('users')
ur=User_register(d)
dd = getListOfFiles('users2')
ur2=User_register(dd)

print(ur)
print("*********************************************************")
print(ur2)

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
print("************************************************************")
print(len(ur2))
        
        
print(ur["bojan.djukic@rt-rk.com"])
ip_adresa= "192.168.100.2"
ur["bojan.djukic@rt-rk.com"]=ip_adresa
devices=["laptop1", " laptop2"]
ur["bojan.djukic@rt-rk.com"]=devices
ur["bojan.djukic@rt-rk.com"]="novo ime kolege"

print(ur.getUser("bojan.djukic@rt-rk.com"))

