import os
from pathlib import Path
from os import environ as environment

from dotenv import load_dotenv


env_path = os.path.join(Path(__file__).parent.parent.parent.parent, ".env")
load_dotenv(override=True, dotenv_path=env_path)

SERVICE_NOTIFICATION_TOKEN = environment["SERVICE_NOTIFICATION_TOKEN"]
