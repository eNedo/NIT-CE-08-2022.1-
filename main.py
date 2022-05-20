import json
import glob
import os
import socket
import re
import ipaddress


class User_register:
   
    def __init__(self,files=""):        #if we don't pass any files, we will create object with no users registered 
        self.users = []                 #each object of User_register has it's own users 
        if files != "":                  
            result=[]
            for single_file in files:
                with open(single_file, 'r') as f:
                    studentDict = json.loads(f.read())
                    result.append(studentDict)
            data=[]
            for x in result: data += (x) 
            for d in data:
                if not self.checkEmail(d['email']):         break #check email and ip address, if invalid skip 
                if not self.validate_ip_address(d['ip']):   break #if valid, insert data into users list 
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
                                for device in new_dev: self.users[i]['devices'].append(device)      #in case of multiple entries in .json files, merge devices
                                #print("we found duplicate: ",new_dev)
                            added=True 
                    if not added:  self.users.append(dict(d))
                    added=True
 
    def setNameSurname(self, email, name): 
        if isinstance(name,str): 
            if  not self.checkEmail(email):   return 
            for user in self.users:
                if user.get("email")==email: 
                    user.update({"name":name})
                    return 
            print("No one is associated with " + email)
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
            ipaddress.ip_address(address)
            return True
        except ValueError:
             print("IP address {} is not valid".format(address))
             return False

    #Validates emails.  
    #TODO!!!!
    def checkEmail(self,email):
        regex = '^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$'
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

    #overloaded + 
    def __add__(self, other): 
        if isinstance(other,User_register): 
            result = User_register() 
            result.users = list(self.users)     #make new list, result.users=self.users won't work 
            for user in other.users: 
                    for userx in self.users: #if user exists, merge devices list 
                        if userx['email']==user['email']: 
                            devices = userx['devices']
                            for device in devices: 
                                if device not in user['devices']: user['devices'].append(device)
                            result.setDevices(userx['email'], user['devices'])
                        else: # if it doesn't already exist, add him 
                            if isinstance(result.getUser(user['email']), str): result.users.append(user)
            return result
        else: 
            print("object is not valid!")
    
    # Overloaded += 
    def __iadd__(self, other): 
        if isinstance(other,User_register): 
            for user in other.users: 
                    for userx in self.users: 
                        if userx['email']==user['email']: 
                            devices = userx['devices']
                            for device in devices: 
                                if device not in user['devices']: user['devices'].append(device)
                            self.setDevices(userx['email'], user['devices'])
                        else: 
                            if isinstance(self.getUser(user['email']), str): self.users.append(user)
            return self
        else: 
            print("object is not valid!")


    def __mul__(self,other): 
        result=User_register()  #empty user register
        for user in self.users: 
            for userx in other.users:
                if userx['email']==user['email']:#if users have same email
                    if userx['ip']==user['ip']: #and same ip adress 
                        temp = userx 
                        devices = user['devices']
                        for device in devices:  #merge their devices 
                            if device not in temp['devices']:   temp['devices'].append(device)
                        result.users.append(temp) #and add them to resulting user register 
                    else: #else, skip the entry and print error message 
                        print(str(user) + " ---- " + str(userx) + "\n Korisnici imaju razlicitu IP adresu!") 
        return result 



def getListOfFiles(foldername): 
    files = glob.glob(os.path.join(foldername,'*'), recursive=True) 
    for file in files: 
        if ".json" not in file: 
            files.remove(file)
    return files 

d2= getListOfFiles('users2')
ur2=User_register(d2)

d1 = getListOfFiles('users1')
ur1=User_register(d1)


rezultat1 = ur1
ur1+=ur2 


print(ur1)

print(len(ur1))
print(len(ur2))
print(len(rezultat1))

presjek = ur1 * ur2 
print(presjek)
