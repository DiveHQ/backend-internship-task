

from fastapi import HTTPException, status


class ValidationError(HTTPException):
  def __init__(self, detail: str):
    self.status_code = status.HTTP_400_BAD_REQUEST
    self.detail = detail

class InvalidCredentialError(HTTPException):
  def __init__(self, detail: str):
    self.status_code = status.HTTP_401_UNAUTHORIZED
    self.detail = detail

class UserNotFoundError(ValidationError):
  pass

class EmptyResponseError(ValidationError):
  pass

class NotFoundError(HTTPException):
   def __init__(self, detail: str):
    self.status_code = status.HTTP_404_NOT_FOUND
    self.detail = detail

class ForbiddenError(HTTPException):
   def __init__(self, detail: str):
    self.status_code = status.HTTP_403_FORBIDDEN
    self.detail = detail


class CredentialsException(HTTPException):
    def __init__(self, detail: str):
        self.detail = detail
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.headers = {"WWW-Authenticate": "Bearer"}
 