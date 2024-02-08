import aiohttp as __aiohttp
import fileuploader.AuthError as AuthError
import fileuploader.exceptions as exceptions

class UploadResponse:
    def __init__(self, response_json):
        self.file_url: str = response_json["file_url"]
        self.file_url_full: str = response_json["file_url_full"]
        self.key: str = response_json["key"]
        self.ext: str = response_json["ext"]
        self.user_filename: str = response_json["user_filename"]
        self.synced: bool = response_json["synced"]
        self.size: str = response_json["size"]
        self.craeted_at: float = response_json["craeted_at"]
        self.auth_error: AuthError.AuthError = (
            AuthError.AuthError(response_json["auth_error"])
            if "auth_error" in response_json and response_json["auth_error"]
            else None
        )

    async def delete(self) -> bool:
        """Deletes file"""
        async with __aiohttp.ClientSession("https://fu.andcool.ru") as session:
            async with session.get(
                f"/api/delete/{self.file_url}?key={self.key}"
            ) as response:
                if response.status == 200:
                    return True

                errors = {
                    400: exceptions.InvalidUniqueKey,
                    404: exceptions.FileNotFound,
                    429: exceptions.TooManyRequests,
                    500: exceptions.InternalServerError,
                    502: exceptions.APIDidntRespond,
                    522: exceptions.ServerDidntRespond,
                }
                raise errors.get(response.status, exceptions.UnhandledError(response.status))

    def __str__(self):
        return f"<UploadResponse file_url:'{self.file_url}' user_filename:'{self.user_filename}'>"
