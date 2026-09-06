from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Annotated, Optional

class CourseBase(BaseModel):

    title: Annotated[str, Field(min_length=1, max_length=100)]
    instructor: Annotated[str, Field(min_length=3, max_length=100)]
    capacity: Annotated[int, Field(gt=0)]
    fee: Annotated[float, Field(ge=0.0)]

    @field_validator('title','instructor')
    @classmethod
    def formatting_title(cls, value: str) -> str:
        return value.strip().title()
    
class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[Annotated[str, Field(min_length=1, max_length=100)]] = None
    instructor: Optional[Annotated[str, Field(min_length=3, max_length=100)]] = None
    capacity: Optional[Annotated[int, Field(gt=0)]] = None
    fee: Optional[Annotated[float, Field(ge=0.0)]] = None

class CourseResponse(CourseBase):
    id: int
    seats_available: int

    class Config:
        from_attributes = True