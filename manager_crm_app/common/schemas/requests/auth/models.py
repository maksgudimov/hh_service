import re
from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator
from fastapi import HTTPException


class UserRegister(BaseModel):
    email: Annotated[EmailStr, Field(..., description="Email address")]
    password: Annotated[str, Field(..., description="Password")]
    password_match: Annotated[str, Field(..., description="Password Match")]
    phone_number: Annotated[str, Field(..., description="Phone number")]
    first_name: Annotated[str, Field(..., description="First name")]
    last_name: Annotated[str, Field(..., description="Last name")]
    username: Annotated[str, Field(..., description="Last name")]
    company_id: Annotated[Optional[int], Field(..., description="Company ID")] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\+\d{5,15}$', value):
            raise HTTPException(
                status_code=400,
                detail="Номер телефона должен начинаться с '+' и содержать от 5 до 15 цифр",
            )
        return value


class UserLogin(BaseModel):
    email: Annotated[EmailStr, Field(..., description="Email address")]
    password: Annotated[str, Field(..., description="Password")]
