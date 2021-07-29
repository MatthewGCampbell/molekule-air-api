import asyncio
import aiohttp 

from molekule import Molekule

async def main():
    async with aiohttp.ClientSession() as session:
        # just for testing
        user_username = input("Username: ")
        user_password = input ("Password: ")
        auth = Molekule(websession=session, host="https://api.molekule.com/users/me")
        # This will fetch data from https://api.molekule.com/users/me/devices
        resp = await auth.request(method="get", username=user_username, password=user_password, path="devices")
        """print HTTP response status code"""
        print("HTTP response status code", resp.status_code)
        """print response JSON content"""
        print("HTTP response JSON content", resp.json())

asyncio.run(main())