import aiohttp as aiohttp
import fileuploader.exceptions as exceptions
from typing import List, Dict
import fileuploader.group as Group

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
            
    async def get_groups(self) -> List[Group.Group]:
        if not self.accessToken:
            raise exceptions.NotAuthorized("No access token provided")
        
        async with aiohttp.ClientSession("https://fu.andcool.ru") as session:
            async with session.get(f"/api/get_groups", headers={"Authorization": "Bearer " + self.accessToken}) as response:
                if response.status != 200:
                    raise exceptions.UnhandledError(await response.json())
                
                groups_list: List[Group.Group] = []
                for group in (await response.json())['groups']:
                    group_obj = Group.Group()
                    group_obj.group_name = group["name"]
                    group_obj.group_id = group["group_id"]
                    groups_list.append(group_obj)

                private_group = Group.Group()
                private_group.group_id = "private"
                private_group.group_name = "private"
                groups_list.insert(0, private_group)
                return groups_list
            
    async def create_group(self, group_name: str) -> Group.Group:
        """Create group"""
        if not self.accessToken:
            raise exceptions.NotAuthorized("No access token provided")
        
        async with aiohttp.ClientSession("https://fu.andcool.ru") as session:
            async with session.post(f"/api/create_group", 
                                    json={"group_name": group_name},
                                    headers={"Authorization": "Bearer " + self.accessToken}) as response:
                if response.status == 200:
                    response_json = await response.json()
                    group = Group.Group()
                    group.group_id = response_json['group_id']
                    group.group_name = response_json['name']
                    return group

                errors = {
                    400: exceptions.Error((await response.json())['message']),
                }
                raise errors.get(response.status, exceptions.UnhandledError(response.status))


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
