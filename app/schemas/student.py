from pydantic import field_validator, Field, BaseModel, EmailStr
from typing import Annotated, Optional

class StudentBase(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=50)]
    email: Annotated[EmailStr, Field(min_length=1, max_length=50)]

    @field_validator('name')
    @classmethod
    def format_name(cls, value):
        return value.strip().title()

    @field_validator('email')
    @classmethod
    def format_email(cls, value):
        return value.strip().lower()

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[Annotated[str, Field(min_length=1, max_length=50)]] = None
    email: Optional[Annotated[EmailStr, Field(min_length=1, max_length=50)]] = None

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True