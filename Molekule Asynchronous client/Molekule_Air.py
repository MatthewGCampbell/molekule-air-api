import asyncio
import requests
import json
from pycognito import Cognito
from datetime import date

molekule_api_url = 'https://api.molekule.com/users/me'

def main():
    