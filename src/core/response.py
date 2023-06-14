
from starlette.responses import JSONResponse

class APIResponse(JSONResponse):
    def __init__(self, data=None, errors=None, status_code=None):
        self.data = data
        self.errors = errors or {}
        self.status_code = status_code

    def to_dict(self):
        return {
            "data": self.data,
            "errors": self.errors,
            "status_code": self.status_code,
        }


