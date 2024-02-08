# File uploader package

Asynchronous Python package for working with the API [fu.andcool.ru](https://fu.andcool.ru). The package is currently in beta.

## Installing
Run `pip install fileuploader` in the console.

## Simple example
Use the `upload` method to upload the file to the server.
```python
import fileuploader
import asyncio


async def run():
    f = open("tests/logo.png", "rb")  # Open file as bytes
    response = await fileuploader.upload(f.read(), f.name)  # Upload file to a fu
    print(response.file_url_full)  # Print file url


asyncio.run(run())

```

## More examples
You can find more usage examples [here](https://github.com/Andcool-Systems/FileUploader-python/tree/main/fileuploader/tests).
