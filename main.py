import json
import glob
import os
import socket
import re
import ipaddress


def get_list_of_files(folder_name):
    files = glob.glob(os.path.join(folder_name, '*'), recursive=True)
    for file in files:
        if ".json" not in file:
            files.remove(file)
    return files


class UserRegister:
    """UserRegister class:
    If we do not pass any files, we will create object with no users registered.
    Each object of UserRegister has its own users.

    :param files: JSON files to be loaded.
    """
    def __init__(self, files=""):
        self.users = []
        if files != "":
            result = []
            for single_file in files:
                with open(single_file, 'r') as f:
                    student_dict = json.loads(f.read())
                    result.append(student_dict)
            data = []
            for x in result:
                data += x
            for d in data:
                if not self.check_email(d['email']):
                    break  # check email and ip address, if invalid skip
                if not self.validate_ip_address(d['ip']):
                    break  # if valid, insert data into users list
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
                                for device in new_dev:
                                    self.users[i]['devices'].append(device)  # in case of multiple entries in .json files, merge devices
                                # print("we found duplicate: ",new_dev)
                            added = True
                    if not added:
                        self.users.append(dict(d))
                    added = True

    def set_name_username(self, email, name):
        """
        Function to set name.
        :param email: Email of the user.
        :param name: Name to be set.
        :return: None if wrong email, email if name setted.
        """
        if isinstance(name, str):
            if not self.check_email(email):
                return None
            for user in self.users:
                if user.get("email") == email:
                    user.update({"name": name})
                    return email
            print("No one is associated with " + email)

    def set_ip(self, email, ip):
        """
        Function to set IP address.
        :param email: Email of the user.
        :param ip: IP address to be set.
        :return: None if wrong email and wrong IP address, IP if set.
        """
        if not self.check_email(email):
            return None
        if not self.validate_ip_address(ip):
            return None
        for user in self.users:
            if user.get("email") == email:
                user.update({"ip": ip})
                return ip

    def set_devices(self, email, devices):
        """

        :param email:
        :param devices:
        :return:
        """
        if isinstance(devices, list):
            valid = True
            if not self.check_email(email):
                return None
            for device in devices:
                if "laptop" not in device and "desktop" not in device and "mobile" not in device:
                    valid = False
            if not valid:
                return "Device tags are not valid!"
            for user in self.users:
                if user.get("email") == email:
                    user.update({"devices": devices})
                    return devices
            return "No devices associated with " + email
        else:
            print("Device argument is not list!")

    def get_name_surname(self, email):
        """
        Function to get name and surname.
        :param email: Email of the user.
        :return: Name and surname for wanted email.
        """
        for user in self.users:
            if user.get("email") == email:
                return user.get("name")
        return "No one is associated with " + email

    def get_devices(self, email):
        """
        Function to get devices.
        :param email: Email of the user.
        :return: Devices associated to wanted email.
        """
        for user in self.users:
            if user.get("email") == email:
                return user.get("devices")
        return "No devices associated with " + email

    def get_ip(self, email):
        """
        Function for getting ip address.
        :param email: Email of the user.
        :return: IP address for wanted email.
        """
        for user in self.users:
            if user.get("email") == email:
                return user.get("ip")
        return "No IP associated with " + email

    def get_user(self, email):
        """
        Function to get user info.
        :param email: Email of the user.
        :return: User info if valid user, No one is associated with + email if non-existing user.
        """
        for user in self.users:
            if user.get("email") == email:
                return user
        return "No one is associated with " + email

    def __str__(self):
        string = ""
        for user in self.users:
            string = string + str(user) + "\n"
        return string

    def validate_ip_address(self, address):
        """Function to validate the IP address.
        :param address: Address to bi validated.
        :return: True if valid, False if invalid.
        """
        try:
            ipaddress.ip_address(address)
            return True
        except ValueError:
            print("IP address {} is not valid".format(address))
            return False

    def check_email(self, email):
        """Function to validate the IP address.
        :param email: Email to be validated.
        :return: True if valid, False if invalid.
        """
        regex = '^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$'
        if re.search(regex, email):
            print("Email {} is not valid".format(email))
            return False
        else:
            return True

    def __len__(self):
        return len(self.users)

    def __getitem__(self, key):
        for i in range(len(self.users)):
            if self.users[i]['email'] == key:
                return self.users[i]

    def __setitem__(self, key, value):
        if isinstance(key, str):
            if not self.check_email(key):
                return None
        else:
            print("Key is not string")
            return None
        if isinstance(value, list):
            self.set_devices(key, value)
        elif isinstance(value, str):
            try:
                socket.inet_aton(value)
                self.set_ip(key, value)
            except socket.error:
                self.set_name_username(key, value)
        else:
            print("Value is not valid")

    # overloaded +
    def __add__(self, other):
        if isinstance(other, UserRegister):
            result = UserRegister()
            result.users = list(self.users)  # make new list, result.users=self.users won't work
            for user in other.users:
                for userx in self.users:  # if user exists, merge devices list
                    if userx['email'] == user['email']:
                        devices = userx['devices']
                        for device in devices:
                            if device not in user['devices']:
                                user['devices'].append(device)
                        result.set_devices(userx['email'], user['devices'])
                    else:  # if it doesn't already exist, add it
                        if isinstance(result.get_user(user['email']), str):
                            result.users.append(user)
            return result
        else:
            print("object is not valid!")

    # Overloaded += 
    def __iadd__(self, other):
        if isinstance(other, UserRegister):
            for user in other.users:
                for userx in self.users:
                    if userx['email'] == user['email']:
                        devices = userx['devices']
                        for device in devices:
                            if device not in user['devices']:
                                user['devices'].append(device)
                        self.set_devices(userx['email'], user['devices'])
                    else:
                        if isinstance(self.get_user(user['email']), str):
                            self.users.append(user)
            return self
        else:
            print("Object is not valid!")

    def __mul__(self, other):
        result = UserRegister()  # empty user register
        for user in self.users:
            for userx in other.users:
                if userx['email'] == user['email']:  # if users have same email
                    if userx['ip'] == user['ip']:  # and same ip adress
                        temp = userx
                        devices = user['devices']
                        for device in devices:  # merge their devices
                            if device not in temp['devices']:
                                temp['devices'].append(device)
                        result.users.append(temp)  # and add them to resulting user register
                    else:  # else, skip the entry and print error message
                        print(str(user) + " ---- " + str(userx) + "\n Korisnici imaju razlicitu IP adresu!")
        return result


d = get_list_of_files('users')
print(d)
ur = UserRegister(d)
print(ur)

d1 = get_list_of_files('users2')
print(d1)
ur1 = UserRegister(d1)
print(ur1)
rws = ur.get_user('nikola.jeftenic@rt-rk.com')
print(rws)
