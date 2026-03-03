from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum


class ReactionsStatus(str, Enum):
    NEW = "новый"
    VIEWED = "просмотрен"
    REJECTED = "отклонён"
