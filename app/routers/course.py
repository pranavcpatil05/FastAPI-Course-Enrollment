from fastapi import FastAPI, APIRouter, HTTPException, status, Depends 
from sqlalchemy.orm import Session
from typing import List

from app.database import get_DB
from app.schemas.course import CourseUpdate, CourseResponse,CourseCreate
from app.models.course import CourseModel

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post('/', response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session=Depends(get_DB)):
    new_course = CourseModel(
        title = course.title,
        instructor = course.instructor,
        capacity = course.capacity,
        fee = course.fee,
        seats_available = course.capacity 
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course

@router.get('/', response_model=List[CourseResponse], status_code=status.HTTP_200_OK)
def getall_course(db: Session=Depends(get_DB)):

    all_courses= db.query(CourseModel).all()
    return all_courses

@router.get('/available', response_model=List[CourseResponse], status_code=status.HTTP_200_OK)
def get_available_courses(db: Session=Depends(get_DB)):
    available_courses = db.query(CourseModel).filter(CourseModel.seats_available>0).all()
    return available_courses

@router.get('/{course_id}', response_model=CourseResponse, status_code=status.HTTP_200_OK)
def get_course(course_id: int, db: Session=Depends(get_DB)):
    data = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Course with ID {course_id} was not found in the database.')
    return data

@router.put('/{course_id}', response_model=CourseResponse, status_code=status.HTTP_200_OK)
def update_course(course_id: int,course_data: CourseUpdate, db: Session=Depends(get_DB)):
    existing_course = db.query(CourseModel).filter(course_id==CourseModel.id).first()

    if not existing_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Course with ID {course_id} was not found in the database.')
    
    update_data_dict = course_data.model_dump(exclude_unset=True)
    
    for key, value in update_data_dict.items():
        setattr(existing_course, key, value)
    if 'capacity' in update_data_dict:
        existing_course.seats_available = existing_course.capacity

    db.commit()
    db.refresh(existing_course)

    return existing_course

@router.delete('/{course_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session=Depends(get_DB)):
    existing_course = db.query(CourseModel).filter(course_id==CourseModel.id).first()
    if not existing_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Course with ID {course_id} was not found in the database.')
    
    db.delete(existing_course)
    db.commit()

    return None


