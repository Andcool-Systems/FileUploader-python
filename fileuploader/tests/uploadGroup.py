import fileuploader
import asyncio


async def run():
    user = await fileuploader.User.login("Username", "Password")  # Log in into an account
    group = (await user.get_groups())[-1]  # Get the last group on account

    f = open("tests/logo.png", "rb")  # Open file as bytes
    response = await fileuploader.upload(f.read(), f.name, user=user, group=group)  # Upload file to a fu, with connecting to a group
    print(response.file_url_full)  # Print file url


asyncio.run(run())
