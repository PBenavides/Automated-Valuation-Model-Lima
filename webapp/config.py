import os

class Config:
    """Config Class
    """
    SECRET_KEY = os.environ.get("SECRET_KEY")