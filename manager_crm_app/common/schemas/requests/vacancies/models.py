from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Annotated, Optional, List
from decimal import Decimal
from datetime import datetime, date


class VacancyCreate(BaseModel):

    title: Annotated[str, Field(
        ...,  # ... означает обязательное поле
        description="Vacancy title",
        min_length=3,
        max_length=255,
        examples=["Python Developer"]
    )]

    description: Annotated[str, Field(
        ...,
        description="Detailed job description",
        min_length=10,
        examples=["We are looking for a Python developer..."]
    )]

    company_name: Annotated[str, Field(
        ...,
        description="Company name",
        max_length=255,
        examples=["Tech Corp"]
    )]

    location: Annotated[Optional[str], Field(
        None,
        description="Job location (city, remote, etc.)",
        max_length=255,
        examples=["Moscow", "Remote", "Saint Petersburg"]
    )]

    salary_from: Annotated[Optional[Decimal], Field(
        None,
        description="Minimum salary",
        gt=0,
        examples=[150000.00]
    )]

    salary_to: Annotated[Optional[Decimal], Field(
        None,
        description="Maximum salary",
        gt=0,
        examples=[250000.00]
    )]

    salary_currency: Annotated[str, Field(
        "RUB",
        description="Currency for salary",
        pattern="^(RUB|USD|EUR)$",
        examples=["RUB", "USD", "EUR"]
    )]

    experience: Annotated[Optional[str], Field(
        None,
        description="Required experience",
        max_length=50,
        examples=["3-5 years", "1+ year", "No experience"]
    )]

    employment: Annotated[str, Field(
        "full_time",
        description="Employment type",
        pattern="^(full_time|part_time|remote|internship)$",
        examples=["full_time", "part_time", "remote"]
    )]

    skills: Annotated[List[str], Field(
        default_factory=list,
        description="Required skills",
        examples=[["Python", "FastAPI", "SQLAlchemy"]]
    )]

    is_active: Annotated[bool, Field(
        True,
        description="Is vacancy active"
    )]

    expires_at: Annotated[Optional[datetime], Field(
        None,
        description="Expiration date",
        examples=["2025-12-31T23:59:59"]
    )]

    company_id: Annotated[int, Field(
        ...,
        description="Company ID",
        gt=0,
        examples=[1]
    )]

    # Валидация зарплаты
    @field_validator('salary_to')
    @classmethod
    def validate_salary_range(cls, v: Optional[Decimal], info):
        if v is not None and info.data.get('salary_from') is not None:
            if v < info.data['salary_from']:
                raise ValueError('salary_to must be greater than or equal to salary_from')
        return v

    # Валидация даты истечения
    @field_validator('expires_at')
    @classmethod
    def validate_expires_at(cls, v: Optional[datetime]):
        if v is not None and v < datetime.now():
            raise ValueError('expires_at must be in the future')
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Senior Python Developer",
                "description": "We are looking for an experienced Python developer...",
                "company_name": "Tech Corp",
                "location": "Moscow",
                "salary_from": 250000,
                "salary_to": 400000,
                "salary_currency": "RUB",
                "experience": "5+ years",
                "employment": "full_time",
                "skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
                "is_active": True,
                "expires_at": "2025-12-31T23:59:59",
                "company_id": 1
            }
        }
    )


class VacancyUpdate(VacancyCreate):
    title: Annotated[Optional[str], Field(
        None,
        description="Vacancy title",
        min_length=3,
        max_length=255
    )]

    description: Annotated[Optional[str], Field(
        None,
        description="Detailed job description",
        min_length=10
    )]

    company_name: Annotated[Optional[str], Field(
        None,
        description="Company name",
        max_length=255
    )]

    location: Annotated[Optional[str], Field(
        None,
        description="Job location",
        max_length=255
    )]

    salary_from: Annotated[Optional[Decimal], Field(
        None,
        description="Minimum salary",
        gt=0
    )]

    salary_to: Annotated[Optional[Decimal], Field(
        None,
        description="Maximum salary",
        gt=0
    )]

    salary_currency: Annotated[Optional[str], Field(
        None,
        description="Currency for salary",
        pattern="^(RUB|USD|EUR)$"
    )]

    experience: Annotated[Optional[str], Field(
        None,
        description="Required experience",
        max_length=50
    )]

    employment: Annotated[Optional[str], Field(
        None,
        description="Employment type",
        pattern="^(full_time|part_time|remote|internship)$"
    )]

    skills: Annotated[Optional[List[str]], Field(
        None,
        description="Required skills"
    )]

    is_active: Annotated[Optional[bool], Field(
        None,
        description="Is vacancy active"
    )]

    expires_at: Annotated[Optional[datetime], Field(
        None,
        description="Expiration date"
    )]

    @field_validator('salary_to')
    @classmethod
    def validate_salary_range(cls, v: Optional[Decimal], info):
        """Валидация зарплаты если оба поля переданы"""
        if v is not None and info.data.get('salary_from') is not None:
            if v < info.data['salary_from']:
                raise ValueError('salary_to must be greater than or equal to salary_from')
        return v

    @field_validator('expires_at')
    @classmethod
    def validate_expires_at(cls, v: Optional[datetime]):
        if v is not None and v < datetime.now():
            raise ValueError('expires_at must be in the future')
        return v
