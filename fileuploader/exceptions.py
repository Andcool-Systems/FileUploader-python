class FileNotFound(Exception):
    """File not found"""
    def __init__(self, message="File not found"):
        self.message = message
        super().__init__(self.message)

class TooManyRequests(Exception):
    """Too many requests"""
    def __init__(self, message="Too many requests"):
        self.message = message
        super().__init__(self.message)

class InternalServerError(Exception):
    """Internal server error"""
    def __init__(self, message="Internal server error"):
        self.message = message
        super().__init__(self.message)

class APIDidntRespond(Exception):
    """API down"""
    def __init__(self, message="The API didn't respond"):
        self.message = message
        super().__init__(self.message)

class ServerDidntRespond(Exception):
    """Server down"""
    def __init__(self, message="The server didn't respond"):
        self.message = message
        super().__init__(self.message)

class InvalidGroup(Exception):
    """Invalid group id"""
    def __init__(self, message="Invalid group Id"):
        self.message = message
        super().__init__(self.message)

class YouAreNotInTheGroup(Exception):
    """You are not in this group"""
    def __init__(self, message="You cannot access this group because you are not a member of it"):
        self.message = message
        super().__init__(self.message)

class GroupNotFound(Exception):
    """Group not found"""
    def __init__(self, message="Group not found"):
        self.message = message
        super().__init__(self.message)

class FileSizeExceedsTheLimit(Exception):
    """File size exceeds the limit (100MiB)"""
    def __init__(self, message="File size exceeds the limit (100MiB)"):
        self.message = message
        super().__init__(self.message)

class InvalidUniqueKey(Exception):
    """Invalid unique key"""
    def __init__(self, message="Invalid file unique key"):
        self.message = message
        super().__init__(self.message)

class UserNotFound(Exception):
    """User not found"""
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)

class WrongPassword(Exception):
    """Wrong password"""
    def __init__(self, message="Wrong password"):
        self.message = message
        super().__init__(self.message)

class NoUsernamePasswordProvided(Exception):
    """No username/password provided"""
    def __init__(self, message="No username/password provided"):
        self.message = message
        super().__init__(self.message)

class Forbidden(Exception):
    """Forbidden"""
    def __init__(self, message="You do not have access to this resource"):
        self.message = message
        super().__init__(self.message)

class AlreadyInGroup(Exception):
    """You are already in the group"""
    def __init__(self, message="It is not possible to accept the invitation because you are already a member of this group"):
        self.message = message
        super().__init__(self.message)


class InvalidLink(Exception):
    """Invite link not found"""
    def __init__(self, message="The link to the invitation was not found"):
        self.message = message
        super().__init__(self.message)

class NotAuthorized(Exception):
    """Invalid access token or token expired+-"""
    def __init__(self, auth_mess, message="Not Authorized: "):
        self.message = "Not Authorized: " + auth_mess
        super().__init__(self.message)

class UserAreadyRegistered(Exception):
    def __init__(self, message="An account with this name is already registered"):
        self.message = message
        super().__init__(self.message)

class UnhandledError(Exception):
    def __init__(self, error_code, message="Unhandled error was occured: Error code"):
        self.message = f"Unhandled error was occured: Error code {error_code}"
        super().__init__(self.message)

class Error(Exception):
    def __init__(self, mess, message=""):
        self.message = f"An error has occured: {mess}"
        super().__init__(self.message)