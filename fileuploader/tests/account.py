import fileuploader
import asyncio


async def run():
    user = await fileuploader.User.register("Username", "Password")  # Create an account with passed username and password
    #user = await fileuploader.User.login("Username", "Password")  # Log in by username and password
    #user = await fileuploader.User.loginToken("<token>")  # You can also log in with an access token
    print(user)


asyncio.run(run())
