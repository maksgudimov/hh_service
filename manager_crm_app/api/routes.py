from typing import List

from api import auth, vacancies, reactions, notifications

from fastapi import APIRouter

from common.schemas.responses.reactions import ReactionResponse
from common.schemas.responses.token import TokenInfo
from common.schemas.responses.vacancies import VacancyResponse

router_auth = APIRouter(prefix="/auth", tags=["Auth"])


router_auth.add_api_route(
    path="/register",
    endpoint=auth.register_user,
    methods=["POST"],
)


router_auth.add_api_route(
    path="/login",
    endpoint=auth.auth_user,
    methods=["POST"],
    response_model=TokenInfo
)


router_vacancies = APIRouter(prefix="/vacancies", tags=["Vacancies"])


router_vacancies.add_api_route(
    path="/list",
    endpoint=vacancies.get_list_vacancies,
    methods=["GET"],
    response_model=List[VacancyResponse],
)

router_vacancies.add_api_route(
    path="/edit/{vacancy_id}",
    endpoint=vacancies.edit_vacancies,
    methods=["PUT"],
)

router_vacancies.add_api_route(
    path="/create",
    endpoint=vacancies.create_vacancies,
    methods=["POST"],
)

router_reactions = APIRouter(prefix="/reactions", tags=["Reactions"])


router_reactions.add_api_route(
    path="/list",
    endpoint=reactions.get_list_reaction,
    methods=["GET"],
    response_model=List[ReactionResponse],
)

router_reactions.add_api_route(
    path="/status/{reaction_id}",
    endpoint=reactions.edit_reaction_status,
    methods=["PATCH"],
)

router_notification_service = APIRouter(prefix="/reactions", tags=["Reactions"])

router_notification_service.add_api_route(
    path="/new",
    endpoint=notifications.get_count_new_reactions,
    methods=["GET"],
)
