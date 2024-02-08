class FileNotFound(Exception):
    """File not found"""
    pass

class TooManyRequests(Exception):
    """Too many requests"""
    pass

class InternalServerError(Exception):
    """Internal server error"""
    pass

class APIDidntRespond(Exception):
    """API down"""
    pass

class ServerDidntRespond(Exception):
    """Server down"""
    pass

class InvalidGroup(Exception):
    """Invalid group id"""
    pass

class YouAreNotInTheGroup(Exception):
    """You are not in this group"""
    pass

class GroupNotFound(Exception):
    """Group not found"""
    pass

class FileSizeExceedsTheLimit(Exception):
    """File size exceeds the limit (100MiB)"""
    pass

class InvalidUniqueKey(Exception):
    """Invalid unique key"""
    pass

class UserNotFound(Exception):
    """User not found"""
    pass

class WrongPassword(Exception):
    """Wrong password"""
    pass

class NoUsernamePasswordProvided(Exception):
    """No username/password provided"""
    pass

class Forbidden(Exception):
    """Forbidden"""
    pass

class AlreadyInGroup(Exception):
    """You are already in the group"""
    pass

class InvalidLink(Exception):
    """Invite link not found"""
    pass

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