from fastapi import HTTPException, status


class NotFoundException(HTTPException):

    def __init__(self, resource: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found.",
        )


class AlreadyExistsException(HTTPException):

    def __init__(self, resource: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{resource} already exists.",
        )


class BusinessRuleException(HTTPException):

    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )