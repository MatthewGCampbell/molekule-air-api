from pycognito import Cognito
import json
import pprint
import requests
from requests.models import Response
from datetime import date
import re
import time

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
number_of_times = 0 # Number of times the loop has run
start_time = time.time()
while True:
    time.sleep(60)
    molekule_api_call()
    if request.status_code == 200:
        print("Successful API Call")
        elapsed_time = time.time() - start_time
        print(elapsed_time)
        number_of_times += 1
        print(number_of_times)
    else:
        print("API Call Failed")
        elapsed_time = time.time() - start_time
        print(elapsed_time)
        exit()