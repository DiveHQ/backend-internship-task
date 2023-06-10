

from fastapi import HTTPException, status


class ValidationError(HTTPException):
  def __init__(self, detail: str):
    super().__init__(detail)
    self.status_code = status.HTTP_400_BAD_REQUEST
    self.detail = detail

class UserNotFoundError(ValidationError):
  pass


class CredentialsException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.headers = {"WWW-Authenticate": "Bearer"}
 