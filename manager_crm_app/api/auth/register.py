from typing import Annotated, Any
from fastapi import Body, Depends
from fastapi.responses import JSONResponse

from api.auth.utils import UserUtils, PasswordUtils
from common.models_manager import UsersManager
from common.schemas.requests.auth.models import UserRegister


async def register_user(
        user_data: Annotated[UserRegister, Body()],
        _: Annotated[Any, Depends(UserUtils.check_has_user)],
        __: Annotated[Any, Depends(UserUtils.check_password_coincidence)],
) -> JSONResponse:
    user_dict = user_data.model_dump(exclude={'password_match'})
    user_dict['password'] = PasswordUtils.get_password_hash(user_data.password)
    await UsersManager.add_user(user_dict)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "User registered successfully",
        }
    )
