from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Student with {enrollment.student_id} Not found in Student Database..')
    
    existing_course = db.query(CourseModel).filter(CourseModel.id == enrollment.course_id).first()
    if not existing_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Course with {enrollment.course_id} Not found in Database..')

    existing_enrollment = db.query(EnrollmentModel).filter(
        EnrollmentModel.course_id == enrollment.course_id,
        EnrollmentModel.student_id == enrollment.student_id
    ).first()

    if existing_enrollment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Student with {enrollment.student_id} has already enrolled in the Course..')

    if existing_course.seats_available <=0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No Seat Available in This Course..')
    
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Student with ID {student_id} is not Found in Database..')
    course_enrolled = db.query(EnrollmentModel).filter(student_id==EnrollmentModel.student_id).all()
    return course_enrolled

@router.get('/{enrollment_id}', response_model=EnrollmentResponse, status_code=status.HTTP_200_OK)
def get_enrollment(enrollment_id: int, db: Session=Depends(get_DB)):
    exiting_enrollment = db.query(EnrollmentModel).filter(enrollment_id==EnrollmentModel.id).first()
    if not exiting_enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Enrollment with {enrollment_id} not found in Enrollment Database..')
    return exiting_enrollment

@router.delete('/{enrollment_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment_id: int, db: Session=Depends(get_DB)):
    existing_enrollment= db.query(EnrollmentModel).filter(enrollment_id==EnrollmentModel.id).first()
    if not existing_enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Enrollment with {enrollment_id} not found in enrollment Database..')
    existing_course = db.query(CourseModel).filter(existing_enrollment.course_id == CourseModel.id).first()
    if existing_course:
        existing_course.seats_available +=1
    db.delete(existing_enrollment)
    db.commit()
    return None