from typing import Annotated, Any

from fastapi import Response, Body, Depends
from fastapi.responses import JSONResponse

from api.auth.utils import UserUtils, JwtUtils
from common.schemas.requests.auth.models import UserLogin
from common.schemas.responses.token import TokenInfo


async def auth_user(
        response: Response,
        user: Annotated[Any, Depends(UserUtils.check_authenticate_user)]
):
    jwt_payload = {
        "sub": user.email,
        "username": user.username,
        "email": user.email,
    }
    token = JwtUtils.encode_jwt(jwt_payload)
    response.set_cookie(key="users_access_token", value=token, httponly=True)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )
