class AuthenticationException(Exception):
    """Base authentication exception."""


class InvalidCredentialsException(AuthenticationException):
    pass


class UserAlreadyExistsException(AuthenticationException):
    pass


class InvalidTokenException(AuthenticationException):
    pass


class UnauthorizedException(AuthenticationException):
    pass


class UserInactiveException(AuthenticationException):
    pass