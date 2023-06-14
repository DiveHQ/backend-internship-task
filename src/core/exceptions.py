from fastapi import HTTPException, status

class ErrorResponse(Exception):
    def __init__(self, status_code=None, data=None, errors=None):
        self.status_code = status_code
        self.data = data
        self.errors = errors or []

    def to_dict(self):
        return {
            "data": self.data,
            "errors": self.errors,
            "status_code": self.status_code,
        }


class CredentialsException(HTTPException):
    def __init__(self, detail: str):
        self.detail = detail
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.headers = {"WWW-Authenticate": "Bearer"}
