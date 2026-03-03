from typing import Annotated

from fastapi import Request, Depends
from common.models import User
from common.models_manager.reactions_manager import ReactionsManager
from common.schemas.responses.reactions import ReactionResponse
from common.utils.users import get_current_auth_user


async def get_list_reaction(
    _: Annotated[User, Depends(get_current_auth_user)]
):
    reactions = await ReactionsManager.get_reactions()
    return [ReactionResponse.model_validate(reaction) for reaction in reactions]
