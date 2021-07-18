# Example of a reverse engineered API call to Cognito to recieve token for Molekule Auth

from pycognito import Cognito
import json
import pprint
import requests
from requests.models import Response
from datetime import date
import re


Attempts = 0

print("Enter your Molekule Credentials Below!")

# Cognito Credentials

def auth_attempts():
    global Attempts
    Attempts += 1
    return Attempts

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Auth Attempts
while Attempts < 3:
    email = input("Enter email: ")
    if(re.match(regex, email)):
            print("Valid Email")
            Attempts = 0 
            break
    else:
        print("Invalid Email")
        auth_attempts()
        continue

u = Cognito('us-west-2_KqrEZKC6r','1ec4fa3oriciupg94ugoi84kkk',
    username=email)

if Attempts >= 3:
    print("Too many attempts. Exiting.")
    exit()

# Password Attempts
while Attempts < 3:
    password = input("Enter password: ")
    try:
        u.authenticate(password=password)
        print("Authenticated")
        Attempts = 0
        break
    except Exception as e:
        print("Error: Wrong Password \n")
        print("Please try again")
        auth_attempts()
        continue
if Attempts >= 3:
    print("Too many attempts. Exiting.")
    exit()

#print your molekule API authorization token (uncomment to see)
print(u.access_token)

url = 'https://api.molekule.com/users/me/devices'
headers = {
    'authorization': u.access_token,
    'x-api-version': '1.0',
    'host': 'api.molekule.com',
    'accept': 'application/json',
    'content-type': 'application/json',
    'user-agent': 'Molekule/3.1.3 (com.molekule.ios; build:1167; iOS 14.0.0) Alamofire/4.9.1',
    'Date': date.today().strftime("%a, %d %b %Y %H:%M:%S GMT")
}

r = requests.get(url, headers=headers)

json_data = json.loads(r.text)

print(json_data)

response_data = r.json()

for element in response_data["content"]:
    serialnumber = element["serialNumber"]
    purifiername = element["subProduct"]["name"]
    device_info = [serialnumber, purifiername]
    print(device_info)
 

PurifierChoice = input("Which Air Purifier do you want to control?")
words = device_info[1].split()
print(words)
if (PurifierChoice == words[0], words[1]):
    print("You have selected the correct Purifier")
elif (PurifierChoice != words[0]):
    print("That Doesnt Exist")
    exit()


fanSpeedUrl = 'https://api.molekule.com/users/me/devices/' +device_info[0] +'/actions' +'/set-fan-speed'
fanSpeedBody = {
    "fanSpeed": 1
}
print(fanSpeedBody)

PowerStatusUrl = 'https://api.molekule.com/users/me/devices/' +device_info[0] +'/actions' +'/set-power-status'
PowerStatusBody = {
    "status": "off"
}
print(PowerStatusBody)


OptionSelection = input("What Would you Like to do?")
if (OptionSelection == "set fan speed"):
    UserInputFanSpeed = input("Which Fan Speed do you want to set? (1-5) \n")
if (OptionSelection == "turn off"):
    UserInputPowerStatus = input("Turn off? (y/n) \n")
    if (UserInputPowerStatus == "y"):
        PowerStatusBody["status"] = "off"
        r = requests.post(PowerStatusUrl, headers=headers, data=json.dumps(PowerStatusBody), verify=True)
if (OptionSelection == "turn on"):
    UserInputPowerStatus = input("Turn on? (y/n) \n")
    if (UserInputPowerStatus == "y"):
        PowerStatusBody["status"] = "on"
        r = requests.post(PowerStatusUrl, headers=headers, data=json.dumps(PowerStatusBody), verify=True)
if (OptionSelection == "exit"):
    exit()

def setfanSpeed(UserInputFanSpeed, serialnumber):
    if UserInputFanSpeed == "1":
        fanSpeedBody["fanSpeed"] = 1
        print(fanSpeedBody)
    elif UserInputFanSpeed == "2":
        fanSpeedBody["fanSpeed"] = 2
        print(fanSpeedBody)
    elif UserInputFanSpeed == "3":
        fanSpeedBody["fanSpeed"] = 3
        print(fanSpeedBody)
    elif UserInputFanSpeed == "4":
        fanSpeedBody["fanSpeed"] = 4
        print(fanSpeedBody)
    elif UserInputFanSpeed == "5":
        fanSpeedBody["fanSpeed"] = 5
        print(fanSpeedBody)
    elif UserInputFanSpeed == "No":
        print("OK, no change")
    elif UserInputFanSpeed <= "0":
        print("No Such Value")
    elif UserInputFanSpeed < "5":
        print("No Such Value")
    r = requests.post(fanSpeedUrl, headers=headers, data=json.dumps(fanSpeedBody), verify=True)
