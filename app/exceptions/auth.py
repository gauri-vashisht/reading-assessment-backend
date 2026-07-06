class AuthenticationException(Exception):
    pass


class InvalidCredentialsException(AuthenticationException):
    pass


class UserAlreadyExistsException(AuthenticationException):
    pass


class UnauthorizedException(AuthenticationException):
    pass