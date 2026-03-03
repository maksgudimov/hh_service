from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, List


class ReactionResponse(BaseModel):
    """
    Модель ответа с данными реакции (отклика)
    """
    id: int
    user_id: Optional[int] = None
    vacancies_id: Optional[int] = None
    email: str
    created_at: datetime
    status: str

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )
