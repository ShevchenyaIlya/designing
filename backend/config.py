import os


class Config:
    """
    Configurations class.
    """

    def __init__(self) -> None:
        self.JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret-key")
        self.APPLICATION_VERSION = os.environ.get("APPLICATION_VERSION", "v2")


CONFIG = Config()
