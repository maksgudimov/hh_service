from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any

from pydantic import Field, BaseModel, ConfigDict


class ResponseBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }
    )


class VacancyResponse(ResponseBase):
    """Ответ с данными вакансии"""
    id: int
    title: str
    description: str
    company_name: str
    location: Optional[str] = None
    salary_from: Optional[Decimal] = None
    salary_to: Optional[Decimal] = None
    salary_currency: str = "RUB"
    experience: Optional[str] = None
    employment: str = "full_time"
    skills: List[str] = Field(default_factory=list)
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    company_id: Optional[int] = None

class VacancyDetailResponse(VacancyResponse):
    """Детальный ответ с дополнительной информацией о компании"""
    company_details: Optional[Dict[str, Any]] = Field(
        None,
        description="Детальная информация о компании"
    )

class VacancyListResponse(ResponseBase):
    """Список вакансий с пагинацией"""
    items: List[VacancyResponse]
    total: int
    page: int
    size: int
    pages: int
    filters: Optional[Dict[str, Any]] = Field(
        None,
        description="Примененные фильтры"
    )

class VacancyCreateResponse(ResponseBase):
    """Ответ после создания вакансии"""
    id: int
    title: str
    message: str = "Vacancy created successfully"
    created_at: datetime

