import fileuploader
import asyncio


async def run():
    user = await fileuploader.User.login("Username", "Password")  # Log in into an account
    
    f = open("tests/logo.png", "rb")  # Open file as bytes
    response = await fileuploader.upload(f.read(), f.name, user=user)  # Upload file to a fu, with connecting to an account
    print(response.file_url_full)  # Print file url


asyncio.run(run())
