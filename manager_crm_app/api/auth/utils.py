import bcrypt

from datetime import timedelta, datetime
from typing import Annotated

import jwt
from fastapi import Body, HTTPException
from starlette import status

from common.models import User
from configs import auth_jwt
from common.schemas.requests.auth.models import UserRegister, UserLogin
from common.models_manager import UsersManager


class JwtUtils:

    @classmethod
    def encode_jwt(
            cls,
            payload: dict,
            private_key: str = auth_jwt.private_key_path.read_text(),
            algorithm: str = auth_jwt.algorithm,
            expire_minutes: int = auth_jwt.access_token_expire_minutes,
            expire_timedelta: timedelta | None = None,
    ):
        to_encode = payload.copy()
        now = datetime.utcnow()
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(
            payload,
            private_key,
            algorithm=algorithm,
        )
        return encoded

    @classmethod
    def decode_jwt(
            cls,
            token: str | bytes,
            public_key: str = auth_jwt.public_key_path.read_text(),
            algorithm: str = auth_jwt.algorithm
    ):
        decoded = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
        )
        return decoded


class PasswordUtils:

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=12)
        hashed_bytes = bcrypt.hashpw(password_bytes, salt)
        return hashed_bytes.decode('utf-8')

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        plain_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_bytes, hashed_bytes)


class UserUtils:

    @classmethod
    async def check_has_user(
            cls,
            user_data: Annotated[UserRegister, Body()],
    ) -> HTTPException | None:
        if await UsersManager.check_user(str(user_data.email)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="user with this email already exists",
            )
        return None

    @classmethod
    def check_password_coincidence(cls, user_data: Annotated[UserRegister, Body()],) -> HTTPException | None:
        if not (user_data.password == user_data.password_match):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="passwords do not match",
            )
        return None

    @classmethod
    async def check_authenticate_user(cls, user_data: Annotated[UserLogin, Body()]) -> HTTPException | User:
        if user := await UsersManager.get_user(str(user_data.email)):
            if not PasswordUtils.verify_password(user_data.password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="password is incorrect",
                )
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="email is incorrect",
        )