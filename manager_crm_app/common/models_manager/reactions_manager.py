from fastapi import HTTPException
from sqlalchemy import select, func
from starlette import status

from common.models import Reactions
from common.schemas.requests.reactions.models import ReactionsUpdate
from configs import database_connection


class ReactionsManager:
    @classmethod
    async def get_reactions(cls):
        async with database_connection.session() as session:
            result = await session.execute(
                select(
                    Reactions
                )
            )
            return result.scalars().all()

    @classmethod
    async def get_count_reactions_with_status(cls, status_reaction: str):
        async with database_connection.session() as session:
            result = await session.execute(
                select(
                    func.count(Reactions.id)
                ).where(
                    Reactions.status == status_reaction
                )
            )
            count = result.scalar()
            return count or 0

    @classmethod
    async def update_status(cls, data: ReactionsUpdate, reaction_id: int):
        async with database_connection.session() as session:
            result = await session.execute(
                select(
                    Reactions
                ).where(
                    Reactions.id == reaction_id
                )
            )
            reaction = result.scalar_one_or_none()
            if not reaction:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            reaction.status = data.status
            await session.commit()
            await session.refresh(reaction)
            return reaction
