from typing import Annotated, Optional

from starlette import status

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator


class Payload(BaseModel):
    chat_id: Annotated[str, Field(..., description="Chat ID")]
    employer_id: Annotated[str, Field(..., description="Employer ID")]
    response_date: Annotated[str, Field(..., description="Response Date")]

    resume_id: Annotated[Optional[str], Field(..., description="Resume ID")] = None
    topic_id: Annotated[str, Field(..., description="Topic ID")]
    vacancy_id: Annotated[Optional[str], Field(..., description="Vacancy ID")] = None


class NewVacancyHHWebhook(BaseModel):
    action_type: Annotated[str, Field(..., description="Action type")]
    id: Annotated[str, Field(..., description="ID")]
    payload: Annotated[Payload, Field(..., description="Payload")]
    subscription_id: Annotated[str, Field(..., description="Subscription ID")]


    @field_validator("id", mode="before")
    @classmethod
    def check_double_id(cls, value):
        # Какая то абстракий проверки дубля, к примеру доставая из Redis
        id_hash = ...
        if id_hash == value:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="double id")
        return value
