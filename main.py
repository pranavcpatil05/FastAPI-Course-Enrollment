from fastapi import FastAPI
from app.database import engine, Base
from app.routers import student_router, course_router, enrollment_router

Base.metadata.create_all(bind = engine)
app = FastAPI(title='Student Enrollment System API')

app.include_router(course_router)
app.include_router(student_router)
app.include_router(enrollment_router)

@app.get('/')
def root():
    return {'message':'Welcome to Student Enrollment System API'}