import json
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.models import Reactions


class ReactionMessageHandlerMQ:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def process_message(self, message_body: bytes) -> bool:
        try:
            data = json.loads(message_body.decode('utf-8'))
            validated_data = await self._validate_reaction_data(data)
            if not validated_data:
                return False
            if await self._is_duplicate(validated_data) is None:
                await self._save_reaction(validated_data)
                return True
            raise Exception(f"Reaction with id {validated_data['reaction_id']} already exists")
        except Exception as e:
            return False

    async def _validate_reaction_data(self, data: dict) -> Optional[dict]:
        try:
            validated = {
                "first_name": data["first_name"],
                "middle_name": data["middle_name"],
                "last_name": data["last_name"],
                "contacts": data["contacts"],
            }
            return validated
        except Exception as e:
            return None

    async def _is_duplicate(self, data: dict) -> bool:
        # Просто пример какого-то запроса в бд, любая логика проверки дублей
        # result = await self.session.execute(
        #     select(
        #         Reactions
        #     ).where(
        #         Reactions.vacancies_id == data["vacancies_id"],
        #         Reactions.user_id == data["user_id"],
        #     )
        # )
        # return result.scalar_one_or_none()
        pass

    async def _save_reaction(self, data: dict):
        reaction = Reactions(
            user_id=data["user_id"],
            vacancies_id=data["vacancies_id"],
            email=data["email"],
            status=data["status"]
        )
        self.session.add(reaction)
        await self.session.commit()
