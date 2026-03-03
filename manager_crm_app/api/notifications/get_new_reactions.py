from typing import Annotated

from fastapi import Request, Depends, Body
from fastapi.responses import JSONResponse
from starlette import status

from common.enums.reactions import ReactionsStatus
from common.models_manager.reactions_manager import ReactionsManager
from common.schemas.requests.notification_service.models import NotificationServiceAuth


async def get_count_new_reactions(
    _: Annotated[NotificationServiceAuth, Body()]
):
    reactions_count = await ReactionsManager.get_count_reactions_with_status(ReactionsStatus.NEW.value)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "success",
            "count": reactions_count
        }
    )
