from typing import Annotated

from fastapi import Request, Depends, Body
from common.models import User
from common.models_manager.reactions_manager import ReactionsManager
from common.schemas.requests.reactions.models import ReactionsUpdate
from common.utils.users import get_current_auth_user

async def edit_reaction_status(
        reaction_id: int,
        _: Annotated[User, Depends(get_current_auth_user)],
        data: Annotated[ReactionsUpdate, Body()],
):
    reaction = await ReactionsManager.update_status(data, reaction_id)
    return reaction
