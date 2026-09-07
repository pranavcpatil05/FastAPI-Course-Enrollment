from app.routers.course import router as course_router
from app.routers.student import router as student_router
from app.routers.enrollment import router as enrollment_router

__all__ = ['course_router','student_router','enrollment_router']