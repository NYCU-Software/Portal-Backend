# pylint: disable=too-few-public-methods

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = False
    ALLOW_CORS = False

class DevelopmentConfig(Config):
    DEBUG = True
    ALLOW_CORS = True

def get_runtime_config():
    return os.getenv("RUNTIME_CONFIG", "Development")
