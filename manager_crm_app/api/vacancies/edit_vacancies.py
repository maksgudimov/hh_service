from typing import Annotated

from fastapi import Request, Depends, Body
from common.models import User
from common.models_manager.vacancies_manager import VacanciesManager
from common.schemas.requests.vacancies.models import VacancyCreate, VacancyUpdate
from common.schemas.responses.vacancies import VacancyResponse
from common.utils.users import get_current_auth_user


async def edit_vacancies(
        vacancy_id: int,
        _: Annotated[User, Depends(get_current_auth_user)],
        data: Annotated[VacancyUpdate, Body()],
):
    vacancy = await VacanciesManager.update_vacancy(data, vacancy_id)
    return vacancy
