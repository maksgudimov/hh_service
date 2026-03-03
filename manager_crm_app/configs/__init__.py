from configs.database.database import database_configuration
from configs.auth_jwt.config import AuthJWTConfig
from configs.database.database_connection import DatabaseConnection

auth_jwt = AuthJWTConfig()

database_connection = DatabaseConnection(configuration=database_configuration)
