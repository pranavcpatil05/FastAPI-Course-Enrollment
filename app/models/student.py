from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class StudentModel(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(50), nullable = False)

    email = Column(String(100), nullable=False, unique=True, index=True)

    enrollments = relationship('EnrollmentModel',back_populates='student')