from dataclasses import dataclass
from urllib.parse import quote


@dataclass
class PostgreSQLConfiguration:
    """Класс для управления конфигурациями базы данных PostgreSQL.

    Args:
        name (str): Имя для PostgreSQL бд.
        username (str): Имя пользователя database аутентификации.
        password (str): Пароль для database аутентификации.
        host (str):  Хост сервера для дб   (default: "localhost").
        port (int): Порт сервера для дб (default: 5432).
        driver (str): Драйвер (default: "psycopg2").

    """
    name: str
    username: str
    password: str
    host: str = "localhost"
    port: int = 5432
    driver: str = "asyncpg"

    def get_uri(self) -> str:
        """Формирование URI для подключение к PostgreSQL.

        Returns:
            str: строка подключения в формате: postgresql+<driver>://<username>:<password>@<host>:<port>/<name>

        """
        uri = f"postgresql+{self.driver}://{self.username}:{quote(self.password)}@{self.host}:{self.port}/{self.name}"
        return uri
