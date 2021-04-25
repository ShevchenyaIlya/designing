import os


class Config:
    def __init__(self) -> None:
        self.JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret-key")


CONFIG = Config()
