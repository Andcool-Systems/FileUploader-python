import aiohttp as aiohttp
import fileuploader.exceptions as exceptions
from . import UploadResponse
from typing import List


class Group:
    def __init__(self):
        self.group_id: str = None
        self.group_name: str = None

    def __str__(self):
        return f"<Group group_name:{self.group_name}, group_id:{self.group_id}>"
    
    async def delete(self, user) -> bool:
        """Delete group"""
        if not self.group_id or not user.accessToken:
            raise exceptions.NotAuthorized("The user or group has not been initialized")
        
        async with aiohttp.ClientSession("https://fu.andcool.ru") as session:
            async with session.post(f"/api/delete_group/{self.group_id}") as response:
                if response.status == 200:
                    return True

                errors = {
                    403: exceptions.Forbidden,
                    404: exceptions.GroupNotFound
                }
                raise errors.get(response.status, exceptions.UnhandledError(response.status))
            
    async def leave(self, user) -> bool:
        """Leave group"""
        if not self.group_id or not user.accessToken:
            raise exceptions.NotAuthorized("The user or group has not been initialized")
        
        async with aiohttp.ClientSession("https://fu.andcool.ru") as session:
            async with session.post(f"/api/leave/{self.group_id}", 
                                   headers={"Authorization": "Bearer " + user.accessToken}) as response:
                if response.status == 200:
                    return True

                errors = {
                    400: exceptions.YouAreNotInTheGroup,
                    401: exceptions.NotAuthorized(""),
                    404: exceptions.GroupNotFound,
                    422: exceptions.InvalidGroup
                }
                raise errors.get(response.status, exceptions.UnhandledError(response.status))
            
    async def get_files(self, user) -> List[UploadResponse.UploadResponse]:
        """Get files in group"""
        if not self.group_id or not user.accessToken:
            raise exceptions.NotAuthorized("The user or group has not been initialized")
        
        async with aiohttp.ClientSession("https://fu.andcool.ru") as session:
            async with session.get(f"/api/get_files/{self.group_id}", 
                                   headers={"Authorization": "Bearer " + user.accessToken}) as response:
                if response.status == 200:
                    files: List[UploadResponse.UploadResponse] = []
                    for file in (await response.json())['data']:
                        files.append(UploadResponse.UploadResponse(file))
                    return files

                errors = {
                    400: exceptions.GroupNotFound,
                    403: exceptions.Forbidden,
                    404: exceptions.GroupNotFound
                }
                raise errors.get(response.status, exceptions.UnhandledError(response.status))
            
    async def generate_invite(self, user):
        """Generate invite in group"""
        if not self.group_id or not user.accessToken:
            raise exceptions.NotAuthorized("The user or group has not been initialized")
        
        async with aiohttp.ClientSession("https://fu.andcool.ru") as session:
            async with session.get(f"/api/generate_invite/{self.group_id}", 
                                   headers={"Authorization": "Bearer " + user.accessToken}) as response:
                if response.status == 200:
                    return InviteLink((await response.json())['invite_link']) 

                errors = {
                    400: exceptions.GroupNotFound,
                    403: exceptions.Forbidden,
                    404: exceptions.GroupNotFound,
                    422: exceptions.InvalidGroup
                }
                raise errors.get(response.status, exceptions.UnhandledError(response.status))

        
class InviteLink:
    def __init__(self, link: str):
        self.link: str = link.split("/")[-1]
        self.link_full = link

    def __str__(self):
        return f"<InviteLink link:{self.link}>"
    
    async def join(self, user) -> Group:
        """Join to the group by invite link"""
        if not user.accessToken:
            raise exceptions.NotAuthorized("The user has not been initialized")
        
        async with aiohttp.ClientSession("https://fu.andcool.ru") as session:
            async with session.post(f"/api/join/{self.link}", 
                                    headers={"Authorization": "Bearer " + user.accessToken}) as response:
                if response.status == 200:
                    response_json = await response.json()
                    group = Group()
                    group.group_id = response_json['group_id']
                    group.group_name = response_json['name']
                    return group

                errors = {
                    400: exceptions.AlreadyInGroup,
                    404: exceptions.InvalidLink
                }
                raise errors.get(response.status, exceptions.UnhandledError(response.status))
            
    async def info(self, user) -> Group:
        """Get info about group by link"""
        if not user.accessToken:
            raise exceptions.NotAuthorized("The user has not been initialized")
        
        async with aiohttp.ClientSession("https://fu.andcool.ru") as session:
            async with session.get(f"/api/invite_info/{self.link}", 
                                    headers={"Authorization": "Bearer " + user.accessToken}) as response:
                if response.status == 200:
                    response_json = await response.json()
                    group = Group()
                    group.group_id = response_json['group_id']
                    group.group_name = response_json['name']
                    return group

                errors = {
                    404: exceptions.InvalidLink
                }
                raise errors.get(response.status, exceptions.UnhandledError(response.status))

