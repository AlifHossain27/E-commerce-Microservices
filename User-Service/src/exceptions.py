from fastapi import HTTPException

class CustomException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class NotFoundException(CustomException):
    def __init__(self, detail: str = "Item not found"):
        super().__init__(status_code=404, detail=detail)

class EntityTooLargeException(CustomException):
    def __init__(self, detail: str = "Request entity too large"):
        super().__init__(status_code=413, detail=detail)

class BadRequestException(CustomException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=400, detail=detail)

class UnauthorizedException(CustomException):
    def __init__(self, detail: str = "Unauthorized access"):
        super().__init__(status_code=401, detail=detail)

class ForbiddenException(CustomException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=403, detail=detail)

class ConflictException(CustomException):
    def __init__(self, detail: str = "Conflict occurred"):
        super().__init__(status_code=409, detail=detail)

class UnprocessableEntityException(CustomException):
    def __init__(self, detail: str = "Unprocessable entity"):
        super().__init__(status_code=422, detail=detail)

class InternalServerErrorException(CustomException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(status_code=500, detail=detail)
