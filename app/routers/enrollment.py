from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from datetime  import date
from app.database  import get_DB
from app.models.enrollment import EnrollmentModel
from app.models.student import StudentModel
from app.models.course import CourseModel
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse

router = APIRouter(prefix='/enrollment',tags=['Enrollments'])

@router.post('/', response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_student(enrollment: EnrollmentCreate, db: Session=Depends(get_DB)):
    existing_student = db.query(StudentModel).filter(StudentModel.id == enrollment.student_id).first()
    if not existing_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Student with ID {enrollment.student_id} was not found in the database.')
    
    existing_course = db.query(CourseModel).filter(CourseModel.id == enrollment.course_id).first()
    if not existing_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Course with ID {enrollment.course_id} was not found in the database.')

    existing_enrollment = db.query(EnrollmentModel).filter(
        EnrollmentModel.course_id == enrollment.course_id,
        EnrollmentModel.student_id == enrollment.student_id
    ).first()

    if existing_enrollment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Student with ID {enrollment.student_id} is already enrolled in this course.')

    if existing_course.seats_available <=0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No seats available for this course.')
    
    existing_course.seats_available -=1

    new_enrollment = EnrollmentModel(
        student_id = enrollment.student_id,
        course_id = enrollment.course_id
    )
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return new_enrollment

@router.get('/', response_model=List[EnrollmentResponse], status_code=status.HTTP_200_OK)
def get_enrollments(db: Session=Depends(get_DB)):
    all_enrollments = db.query(EnrollmentModel).all()
    return all_enrollments

@router.get('/student/{student_id}', response_model=List[EnrollmentResponse], status_code=status.HTTP_200_OK)
def get_enrollment_by_student(student_id: int, db: Session=Depends(get_DB)):
    existing_student = db.query(StudentModel).filter(student_id==StudentModel.id).first()
    if not existing_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Student with ID {student_id} was not found in the database.')
    course_enrolled = db.query(EnrollmentModel).filter(student_id==EnrollmentModel.student_id).all()
    return course_enrolled

@router.get('/{enrollment_id}', response_model=EnrollmentResponse, status_code=status.HTTP_200_OK)
def get_enrollment(enrollment_id: int, db: Session=Depends(get_DB)):
    exiting_enrollment = db.query(EnrollmentModel).filter(enrollment_id==EnrollmentModel.id).first()
    if not exiting_enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Enrollment with ID {enrollment_id} was not found in the database.')
    return exiting_enrollment

@router.delete('/{enrollment_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment_id: int, db: Session=Depends(get_DB)):
    existing_enrollment= db.query(EnrollmentModel).filter(enrollment_id==EnrollmentModel.id).first()
    if not existing_enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Enrollment with ID {enrollment_id} was not found in the database.')
    existing_course = db.query(CourseModel).filter(existing_enrollment.course_id == CourseModel.id).first()
    if existing_course:
        existing_course.seats_available +=1
    db.delete(existing_enrollment)
    db.commit()
    return None