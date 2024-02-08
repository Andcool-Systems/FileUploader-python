import fileuploader
import asyncio


async def run():
    f = open("tests/logo.png", "rb")  # Open file as bytes
    response = await fileuploader.upload(f.read(), f.name)  # Upload file to a fu
    print(response.file_url_full)  # Print file url


asyncio.run(run())
