from typing import Annotated, Any

from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from common.models_manager import UsersManager


from api.auth.utils import JwtUtils


async def get_current_token_payload(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    payload = JwtUtils.decode_jwt(token)
    return payload


async def get_current_auth_user(payload: Annotated[dict, Depends(get_current_token_payload)]):
    email: str | None = payload.get("sub")
    if user := await UsersManager.get_user(email):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid",
    )

