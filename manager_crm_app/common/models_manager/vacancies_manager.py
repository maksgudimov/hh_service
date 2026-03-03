from fastapi import HTTPException
from sqlalchemy import select
from starlette import status

from common.models import Vacancy
from common.schemas.requests.vacancies.models import VacancyCreate, VacancyUpdate
from configs import database_connection


class VacanciesManager:
    @classmethod
    async def get_vacancies(cls):
        async with database_connection.session() as session:
            result = await session.execute(
                select(
                    Vacancy
                )
            )
            return result.scalars().all()

    @classmethod
    async def create_vacancy(cls, payload: dict):
        async with database_connection.session() as session:
            vacancy = Vacancy(**payload)
            session.add(vacancy)
            await session.commit()
            await session.refresh(vacancy)
            return vacancy

    @classmethod
    async def update_vacancy(cls, payload: VacancyUpdate, vacancy_id: int):
        async with database_connection.session() as session:
            result = await session.execute(
                select(
                    Vacancy
                ).where(
                    Vacancy.id == vacancy_id,
                    Vacancy.company_id == payload['company_id'],
                )
            )
            vacancy = result.scalar_one_or_none()
            if not vacancy:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Vacancy with id {vacancy_id} and company id {payload['company_id']} not found"
                )
            update_data = payload.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(vacancy, field, value)
            await session.commit()
            await session.refresh(vacancy)
            return vacancy
