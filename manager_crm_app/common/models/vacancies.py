from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from common.models.base import Base


class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    company_name = Column(String(255), nullable=False)
    location = Column(String(255))
    salary_from = Column(Numeric(10, 2))
    salary_to = Column(Numeric(10, 2))
    salary_currency = Column(String(3), default="RUB")
    experience = Column(String(50))  # "1-3 года"
    employment = Column(String(50), default="full_time")
    skills = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    expires_at = Column(DateTime(timezone=True))  # Дата истечения
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="vacancies", lazy="selectin")

    def __repr__(self):
        return f"Vacancy {self.id}: {self.title}"


class Company(Base):
    """Модель компании (минимальная)"""
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    website = Column(String(255))
    vacancies = relationship("Vacancy", back_populates="company", lazy="selectin")

    def __repr__(self):
        return f"Company {self.id}: {self.name}"
