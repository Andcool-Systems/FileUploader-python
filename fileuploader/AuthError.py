from typing import Dict

class AuthError:
    def __init__(self, auth_error: Dict[str, int]):
        """Auth error class"""
        self.message = None
        self.error_id = None
        if auth_error:
            self.message = auth_error['message']
            self.error_id = auth_error['errorId']

    def __str__(self):
        return f"<AuthError message:'{self.message}' error_id:{self.error_id}>"
