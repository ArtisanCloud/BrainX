from enum import Enum


class AppEnvironment(str, Enum):
    LOCAL = "local"
    PREVIEW = "preview"
    PRODUCTION = "production"
