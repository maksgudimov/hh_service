from typing import Annotated

from fastapi import Request, Depends, Body
from common.models import User
from common.models_manager.vacancies_manager import VacanciesManager
from common.schemas.requests.vacancies.models import VacancyCreate
from common.schemas.responses.vacancies import VacancyResponse
from common.utils.users import get_current_auth_user


async def create_vacancies(
        _: Annotated[User, Depends(get_current_auth_user)],
        data: Annotated[VacancyCreate, Body()],
):
    vacancy = await VacanciesManager.create_vacancy(data.model_dump())
    return vacancy
