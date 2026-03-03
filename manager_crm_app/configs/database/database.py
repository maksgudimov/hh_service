import os
from os import environ as environment
from pathlib import Path

from dotenv import load_dotenv

from configs.database.postgresql_configuration import PostgreSQLConfiguration

env_path = os.path.join(Path(__file__).parent.parent.parent.parent, ".env")
load_dotenv(override=True, dotenv_path=env_path)

database_configuration = PostgreSQLConfiguration(
    host=environment["DB_HOST"],
    port=int(environment["DB_PORT"]),
    username=environment["DB_USERNAME"],
    password=environment["DB_PASSWORD"],
    driver="asyncpg",
    name="core"
)
