from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func

from common.enums.reactions import ReactionsStatus
from common.models.base import Base


class Reactions(Base):
    __tablename__ = "reactions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    vacancies_id = Column(Integer, ForeignKey('vacancies.id'))
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    status = Column(
        String(25),
        default=ReactionsStatus.NEW.value,
        server_default=ReactionsStatus.NEW.value,
        nullable=False
    )
