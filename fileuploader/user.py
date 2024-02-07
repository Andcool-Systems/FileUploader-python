import aiohttp as aiohttp
import fileuploader.exceptions as exceptions
from typing import List, Dict

class User:
    def __init__(self):
        self.username = None
        self.accessToken = None

    def __str__(self):
        return f"<User username:'{self.username}'>"
    
    async def logout(self) -> bool:
        """Logs out from account"""
        if not self.accessToken:
            raise exceptions.NotAuthorized("No access token provided")
        
        async with aiohttp.ClientSession("https://fu.andcool.ru") as session:
            async with session.post(f"/api/logout", headers={"Authorization": "Bearer " + self.accessToken}) as response:
                if response.status == 401 or response.status == 200:
                    self.accessToken = None
                return response.status == 401 or response.status == 200
                
    async def transfer(self, data: List[Dict[str, str]]) -> list:
        """Transfers local files to an account"""
        if not self.accessToken:
            raise exceptions.NotAuthorized("No access token provided")
        
        async with aiohttp.ClientSession("https://fu.andcool.ru") as session:
            async with session.post(f"/api/transfer", headers={"Authorization": "Bearer " + self.accessToken},
                                    json={
                                        "data": data
                                    }) as response:
                if response.status != 200:
                    raise exceptions.UnhandledError(await response.json())
                return (await response.json())['unsuccess']


async def login(username: str, password: str, is_bot: bool = False) -> User:
    """Log in by username and password"""
    async with aiohttp.ClientSession("https://fu.andcool.ru") as session:
        async with session.post(f"/api/login?bot={str(is_bot).lower()}", 
                                json={"username": username,
                                      "password": password}) as response:
            if response.status == 200:
                response_json = await response.json()
                user = User()
                user.username = response_json['username']
                user.accessToken = response_json['accessToken']
                return user

            errors = {
                400: exceptions.NoUsernamePasswordProvided,
                403: exceptions.WrongPassword,
                404: exceptions.UserNotFound,
                500: exceptions.InternalServerError,
                502: exceptions.APIDidntRespond,
                522: exceptions.ServerDidntRespond
            }
            raise errors.get(response.status, exceptions.UnhandledError(response.status))
        

async def register(username: str, password: str, is_bot: bool = False) -> User:
    """Register by username and password"""
    async with aiohttp.ClientSession("https://fu.andcool.ru") as session:
        async with session.post(f"/api/register?bot={str(is_bot).lower()}", 
                                json={"username": username,
                                      "password": password}) as response:
            if response.status == 200:
                response_json = await response.json()
                user = User()
                user.username = response_json['username']
                user.accessToken = response_json['accessToken']
                return user

            errors = {
                400: exceptions.UserAreadyRegistered(),
                404: exceptions.UserNotFound,
                500: exceptions.InternalServerError,
                502: exceptions.APIDidntRespond,
                522: exceptions.ServerDidntRespond
            }
            raise errors.get(response.status, exceptions.UnhandledError(response.status))
        

async def refresh_token(token: str) -> str:
    """Refreshes an access token"""
    async with aiohttp.ClientSession("https://fu.andcool.ru") as session:
        async with session.post(f"/api/refresh_token", 
                                json={"accessToken": token}) as response:
            if response.status == 200:
                response_json = await response.json()
                return response_json['accessToken']

            raise exceptions.UnhandledError(response.status)
