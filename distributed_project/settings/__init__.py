import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]

try:
    os.environ["PROD"]
    from .prod import *  # noqa: F403
except KeyError:
    from .dev import *  # noqa: F403
