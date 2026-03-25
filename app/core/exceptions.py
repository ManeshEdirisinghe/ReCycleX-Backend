from typing import Any, Dict, Optional
from fastapi import HTTPException

class AppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(status_code=status_code, detail=message)
        self.code = code
        self.message = message
        self.details = details

class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found", details: Optional[Dict] = None):
        super().__init__(status_code=404, code="NOT_FOUND", message=message, details=details)

class BadRequestException(AppException):
    def __init__(self, message: str = "Bad request", details: Optional[Dict] = None):
        super().__init__(status_code=400, code="BAD_REQUEST", message=message, details=details)

class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized", details: Optional[Dict] = None):
        super().__init__(status_code=401, code="UNAUTHORIZED", message=message, details=details)

class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden", details: Optional[Dict] = None):
        super().__init__(status_code=403, code="FORBIDDEN", message=message, details=details)
