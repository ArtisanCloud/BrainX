import json


class AppException(Exception):
    def __init__(self, status_code: int = 400, message: str = None):
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return (
            json.dumps({"exception_name": str(self.__class__.__name__),
                        "exception_msg": self.message,
                        "exception_status_code": self.status_code})
        )


class AuthException(AppException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(status_code=400001, message=message)


class ProviderNotFoundException(AppException):
    def __init__(self, message: str = "未找到对应模型提供方，需要配置模型"):
        super().__init__(status_code=400002, message=message)
