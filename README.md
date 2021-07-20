# molekule-air-api
Currently Testing with the Molekule IOS App, the authorization for their API seems to be AWS Cognito

## make sure you have theses libraries 

```python
from pycognito import Cognito
import json
import pprint
import requests
from requests.models import Response
from datetime import date
import re
```
then download or clone this repository and run the `python-molekule-api-example.py` [here](./python-molekule-api-example.py)


BETA STILL WORKING ON DOCS AND MAKING IT BETTER BE PATIENT BUT STILL FEEL FREE TO TEST, still basically CLI based

```shell
First Enter your email you use for your molekule account then your password 
Enter your Molekule Credentials Below!
Enter email: Email
Valid Email
Enter password: Password
```
> Expect a large character string (thats your access token being prited out for debugging)
> Expect some text in JSON format (Should show your vairous Molekule Products)
# then you can type things such as set fan speed, turn off, turn on , and exit (Case Sensitive at least right now)


THIS IS IN NO WAY part of Molekule. its just a project I have done in my free time
