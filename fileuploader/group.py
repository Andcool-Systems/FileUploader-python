import aiohttp as aiohttp
import fileuploader.exceptions as exceptions
import fileuploader.user as User

class Group:
    def __init__(self):
        self.group_id: str = None
        self.group_name: str = None

    async def delete(self, user: User.User) -> bool:
        """Delete group"""
        if not self.group_id or not user.accessToken:
            raise exceptions.NotAuthorized
        
        async with aiohttp.ClientSession("https://fu.andcool.ru") as session:
            async with session.post(f"/api/delete_group/{self.group_id}") as response:
                if response.status == 200:
                    return True

                errors = {
                    403: exceptions.Forbidden,
                    404: exceptions.GroupNotFound
                }
                raise errors.get(response.status, exceptions.UnhandledError(response.status))


async def create_group(group_name: str, group_nameis_bot: bool = False) -> Group:
    """Create group"""
    async with aiohttp.ClientSession("https://fu.andcool.ru") as session:
        async with session.post(f"/api/create_group", 
                                json={"group_name": group_name}) as response:
            if response.status == 200:
                response_json = await response.json()
                group = Group()
                group.group_id = response_json['group_id']
                group.group_name = response_json['name']
                return group

            errors = {
                400: exceptions.Error((await response.json())['message']),
            }
            raise errors.get(response.status, exceptions.UnhandledError(response.status))       
