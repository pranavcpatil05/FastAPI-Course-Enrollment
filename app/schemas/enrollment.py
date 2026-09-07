from pydantic import Field, BaseModel
from typing import Annotated, Optional
from datetime import date

class EnrollmentBase(BaseModel):
    student_id: int 
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentResponse(EnrollmentBase):
    enrollment_id: int = Field(..., validation_alias='id')
    student_id: int
    course_id: int
    enrollment_date: date
    status: str

    class Config:
        from_attributes = True