from sqlalchemy import select

from common.models import User
from configs import database_connection


class UsersManager:
    """
        Класс запросов к модели User
    """
    @classmethod
    async def check_user(cls, email: str) -> bool:
        async with database_connection.session() as session:
            result = await session.execute(
                select(
                    User
                ).where(
                    User.email == email
                )
            )
            user = result.scalar_one_or_none()
            return user is not None

    @classmethod
    async def add_user(cls, user: dict) -> None:
        async with database_connection.session() as session:
            user = User(
                email=user["email"],
                password=user["password"],
                phone_number=user["phone_number"],
                first_name=user["first_name"],
                last_name=user["last_name"],
                username=user["username"],
                company_id=user.get("company_id", None),
            )
            session.add(user)
            await session.commit()

    @classmethod
    async def get_user(cls, email: str) -> User | None:
        async with database_connection.session() as session:
            result = await session.execute(
                select(
                    User
                ).where(
                    User.email == email
                )
            )
            user = result.scalar_one_or_none()
            return user
