from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from app.database import Base
from datetime import date

class EnrollmentModel(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    enrollment_date = Column(Date, default=date.today, nullable=False)
    status = Column(String, default="enrolled", nullable=False)

    course = relationship('CourseModel', back_populates='enrollments')
    student = relationship('StudentModel', back_populates='enrollments')

    @property
    def student_name(self) -> str:
        return self.student.name if self.student else ""

    @property
    def course_title(self) -> str:
        return self.course.title if self.course else ""