from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Annotated
from starlette import status

from configs.service.notification import SERVICE_NOTIFICATION_TOKEN


class NotificationServiceAuth(BaseModel):
    token: Annotated[str, Field(..., description="token service")]

    @field_validator("token", mode="before")
    @classmethod
    def status_validator(cls, value):
        if value != SERVICE_NOTIFICATION_TOKEN:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return value
