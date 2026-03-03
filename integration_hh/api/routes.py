from typing import List

from fastapi import APIRouter
from api import hh


router_hh = APIRouter(prefix="/webhook", tags=["Auth"])


router_hh.add_api_route(
    path="/hh",
    endpoint=hh.add_new_vacancy,
    methods=["POST"],
)
