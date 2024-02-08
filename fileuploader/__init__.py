"""
file uploader

Package for working with the API fu.andcool.ru
"""

import aiohttp as __aiohttp
import fileuploader.UploadResponse as UploadResponse
import fileuploader.exceptions as exceptions
import fileuploader.user as User
import fileuploader.AuthError as AuthError
import fileuploader.group as Group

__version__ = "0.1.2.1"
__author__ = 'AndcoolSystems'


async def upload(bytes: bytes, filename: str, user: User.User = None, group: Group.Group = None) -> UploadResponse.UploadResponse:
    form_data = __aiohttp.FormData()
    form_data.add_field('file', bytes, filename=filename)

    headers = {}
    group_id = "private"
    if user and user.accessToken:
        headers = {"Authorization": "Bearer " + user.accessToken}
        if group and group.group_id:
            group_id = group.group_id

    async with __aiohttp.ClientSession("https://fu.andcool.ru") as session:
        async with session.post(f"/api/upload/{group_id}", 
                                data=form_data, headers=headers) as response:
            if response.status == 200:
                return UploadResponse.UploadResponse(await response.json())
            
            errors = {  # List of known errors
                400: exceptions.InvalidGroup,
                401: exceptions.NotAuthorized(await response.json()['auth_error']),
                403: exceptions.YouAreNotInTheGroup,
                404: exceptions.GroupNotFound,
                413: exceptions.FileSizeExceedsTheLimit,
                429: exceptions.TooManyRequests,
                500: exceptions.InternalServerError,
                502: exceptions.APIDidntRespond,
                522: exceptions.ServerDidntRespond
            }
            raise errors.get(response.status, exceptions.UnhandledError(response.status))
        

async def delete(file_url: str, key: str) -> bool:
    """Deletes file"""
    async with __aiohttp.ClientSession("https://fu.andcool.ru") as session:
        async with session.get(f"/api/delete/{file_url}?key={key}") as response:
            if response.status == 200:
                return True

            errors = {
                400: exceptions.InvalidUniqueKey,
                404: exceptions.FileNotFound,
                500: exceptions.InternalServerError,
                502: exceptions.APIDidntRespond,
                522: exceptions.ServerDidntRespond
            }
            raise errors.get(response.status, exceptions.UnhandledError(response.status))
            