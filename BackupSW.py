#! /usr/bin/env python
from netmiko import Netmiko
from getpass import getpass
from pathlib import Path
from datetime import datetime
import requests
#getting datetime current to Create Folder Backup
currentDay = datetime.now().strftime('%d')
currentMonth = datetime.now().strftime('%h')
currentYear = datetime.now().strftime('%Y')
TimeBK = currentYear + "-" + currentMonth + "-" + currentDay

#open file contaning device IP
pathlistdev = input("Please input path folder devlist: ") + "\devlist.txt"
devlist = open(pathlistdev,"r")

#Folder save file Backup
PathBK = input("Please input path folder save backup: ") + "\\" + TimeBK + "\\"
Path(PathBK).mkdir(parents=True, exist_ok=True)

#getting required information from user to connect devices
username = input("Please enter device username: ")
password = getpass("Please enter device password: ")

#by for loop check each line of device IP text file to find IP address
#and then connect by netmiko to device and downloadig running configuration
#of device and creat a new file in pefered path and name it by IP address of
#device
flag = True
for line in devlist:
        if '@' in line:
                flag = False
                continue
        #Looking for hostname in text file and extract it to a variable
        starthost=line.find('"Hostname":"')
        host_loc_first = (starthost) + 12
        endhost = line.find('","')
        host_loc_end = (endhost) -0
        hostnamebk = line[(host_loc_first):(host_loc_end)]

        #looking for ip address in text file and extract it to a variable
        Location_1=line.find('"ip":"')
        ip_loc_first = (Location_1) + 6
        Location_2=line.find('"..')
        ip_loc_end= (Location_2)- 3
        ip = line[(ip_loc_first):( ip_loc_end)]
        if flag == True:
                #connecting to device by netmiko
                connection = Netmiko(**{"device_type":"cisco_ios","ip": ip,"username": username,"password": password,})
                out = connection.send_command("show running-config")

                pathfilebk = PathBK + hostnamebk + ".cfg"
                file = open(pathfilebk ,"w")

                #creating file to save configuration
                file.write(out)
                file.close()
                connection.disconnect()
        else:      
                url = 'http://' + ip + '/iss.conf'
                r = requests.get(url, allow_redirects=True)
                pathfilebk = PathBK + hostnamebk + ".cfg"
                open(pathfilebk, 'wb').write(r.content)
                
        print("BK host: %s done" %hostnamebk)
#Close file device list
devlist.close()
