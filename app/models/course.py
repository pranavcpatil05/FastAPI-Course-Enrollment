from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from app.database import Base

class CourseModel(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(50),nullable=False)

    instructor = Column(String(50), nullable=False)

    capacity = Column(Integer, nullable=False)

    seats_available = Column(Integer, nullable=False)

    fee = Column(Float, nullable=False)

    enrollments = relationship('EnrollmentModel', back_populates='course')