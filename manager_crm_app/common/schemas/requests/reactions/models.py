from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Annotated, Optional, List
from decimal import Decimal
from datetime import datetime, date

from starlette import status

from common.enums.reactions import ReactionsStatus


class ReactionsUpdate(BaseModel):
    status: Annotated[str, Field(..., description="status reaction")]

    @field_validator("status", mode="before")
    @classmethod
    def status_validator(cls, value):
        if value not in [ReactionsStatus.NEW, ReactionsStatus.REJECTED, ReactionsStatus.VIEWED]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="status reaction must be 'новый' or 'просмотрен' or 'отклонён'",
            )
        return value
