# Example of a reverse engineered API call to Cognito to recieve token for Molekule Auth

from pycognito import Cognito
import json
import pprint
import requests
from requests.models import Response
from datetime import date
import re

debug = True
molekule_api_url = 'https://api.molekule.com/users/me'
print("Enter your Molekule Credentials Below!")
def set_headers(access_token):
    global headers
    headers = {
        'authorization': access_token,
        'x-api-version': '1.0',
        'host': 'api.molekule.com',
        'accept': 'application/json',
        'content-type': 'application/json',
        'user-agent': 'Molekule/3.1.3 (com.molekule.ios; build:1167; iOS 14.0.0) Alamofire/4.9.1',
        'Date': date.today().strftime("%a, %d %b %Y %H:%M:%S GMT")
    }

def check_user_email():
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    Attempts = 0
    while True:
        global email
        email = input("Enter your email: ")
        global u
        if(re.match(regex, email)):
            print("Valid Email")
            # Cognito Credentials
            u = Cognito('us-west-2_KqrEZKC6r', '1ec4fa3oriciupg94ugoi84kkk',username=email)
            Attempts = 0
            break
        elif Attempts <= 3:
            print("Invalid Email")
            Attempts += 1
            continue
        elif Attempts >= 3:
            print("Too many attempts")
            exit()
def check_user_password(email):
    global u
    Attempts = 0
    while True:
        while Attempts < 3:
            password = input("Enter your password: ")
            try:
                u.authenticate(password=password)
                print("Valid Password")
                return
            except Exception as e:
                print("Invalid Password")
                print(e)
                Attempts += 1
                print(Attempts)
                continue
        if Attempts >= 3:
            print("Too many attempts")
            exit()
        if Attempts >= 3:
            print("Too many attempts")
            exit()

# Ask for user input and check if it is valid
check_user_email()
check_user_password(email)


# print your molekule API authorization token (uncomment to see)
if debug:
    print(u.access_token)


def molekule_api_call():
    device_info_url = molekule_api_url + '/devices'
    set_headers(u.access_token)
    global request
    request = requests.get(device_info_url, headers=headers)


molekule_api_call()
json_data = json.loads(request.text)

print(json_data)

response_data = request.json()

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


fanSpeedUrl = 'https://api.molekule.com/users/me/devices/' + device_info[0] + '/actions' + '/set-fan-speed'
fanSpeedBody = {
    "fanSpeed": 1
}


PowerStatusUrl = 'https://api.molekule.com/users/me/devices/' + device_info[0] + '/actions' + '/set-power-status'
PowerStatusBody = {
    "status": "off"
}



def setfanSpeed(InputFanSpeed):
    global fanSpeedBody
    if InputFanSpeed == "1":
        fanSpeedBody["fanSpeed"] = 1
        print(fanSpeedBody)
    elif InputFanSpeed == "2":
        fanSpeedBody["fanSpeed"] = 2
        print(fanSpeedBody)
    elif InputFanSpeed == "3":
        fanSpeedBody["fanSpeed"] = 3
        print(fanSpeedBody)
    elif InputFanSpeed == "4":
        fanSpeedBody["fanSpeed"] = 4
        print(fanSpeedBody)
    elif InputFanSpeed == "5":
        fanSpeedBody["fanSpeed"] = 5
        print(fanSpeedBody)
    elif InputFanSpeed == "No":
        print("OK, no change")
    elif InputFanSpeed <= "0":
        print("No Such Value")
    elif InputFanSpeed < "5":
        print("No Such Value")

while True:
    OptionSelection = input("What Would you Like to do?")
    if (OptionSelection == "set fan speed"):
        UserInputFanSpeed = input("Which Fan Speed do you want to set? (1-5) \n")
        print(serialnumber)
        setfanSpeed(UserInputFanSpeed)
        r = requests.post(fanSpeedUrl, headers=headers,
            data=json.dumps(fanSpeedBody), verify=True)
    if (OptionSelection == "turn off"):
        UserInputPowerStatus = input("Turn off? (y/n) \n")
        if (UserInputPowerStatus == "y"):
            PowerStatusBody["status"] = "off"
            r = requests.post(PowerStatusUrl, headers=headers,
                            data=json.dumps(PowerStatusBody), verify=True)
    if (OptionSelection == "turn on"):
        UserInputPowerStatus = input("Turn on? (y/n) \n")
        if (UserInputPowerStatus == "y"):
            PowerStatusBody["status"] = "on"
            print(PowerStatusBody)
            r = requests.post(PowerStatusUrl, headers=headers,
                            data=json.dumps(PowerStatusBody), verify=True)
    if (OptionSelection == "exit"):
        exit()
