from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date
from app.database import Base

class EnrollmentModel(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer,ForeignKey('students.id') )

    course_id = Column(Integer, ForeignKey('courses.id'))

    enrollment_date = Column(Date, nullable=False)

    status = Column(String, nullable=False)

    course = relationship('CourseModel', back_populates='enrollments')
    student = relationship('StudentModel', back_populates='enrollments')