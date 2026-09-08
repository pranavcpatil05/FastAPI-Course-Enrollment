from pydantic import Field, BaseModel, ConfigDict
from datetime import date

class EnrollmentBase(BaseModel):
    student_id: int 
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentResponse(EnrollmentBase):
    enrollment_id: int = Field(..., validation_alias='id')
    student_id: int
    student_name: str
    course_id: int
    course_title: str
    enrollment_date: date
    status: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)