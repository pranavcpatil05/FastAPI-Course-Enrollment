from app.models.course import router as course_router
from app.models.student import router as student_router
from app.models.enrollment import router as enrollment_router

__all__ = ['course_router','student_router','enrollment_router']