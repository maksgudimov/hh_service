from typing import Annotated

from fastapi import Request, Depends
from common.models import User
from common.models_manager.vacancies_manager import VacanciesManager
from common.schemas.responses.vacancies import VacancyResponse
from common.utils.users import get_current_auth_user


async def get_list_vacancies(
    user: Annotated[User, Depends(get_current_auth_user)]
):
    vacancies = await VacanciesManager.get_vacancies()
    return [VacancyResponse.model_validate(vacancy) for vacancy in vacancies]
