import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    AUTH = os.getenv("AUTH", {})
