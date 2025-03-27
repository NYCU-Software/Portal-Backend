# pylint: disable=too-few-public-methods

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HYDRA_ADMIN = os.getenv("HYDRA_ADMIN")
    HYDRA_PUBLIC = os.getenv("HYDRA_PUBLIC")
    KRATOS_URL = os.getenv("KRATOS_URL")

    DEBUG = False
    ALLOW_CORS = False

class DevelopmentConfig(Config):
    DEBUG = True
    ALLOW_CORS = True

def get_runtime_config():
    return os.getenv("RUNTIME_CONFIG", "Development")
