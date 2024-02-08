import fileuploader
import asyncio


async def run():
    user = await fileuploader.User.register("Username", "Password")  # Create an account with passed username and password
    print(user)


asyncio.run(run())
