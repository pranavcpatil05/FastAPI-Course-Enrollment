from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_DB
from app.models.student import StudentModel
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate

router = APIRouter(prefix='/students', tags=['Students'])

@router.get('/', response_model=List[StudentResponse], status_code=status.HTTP_200_OK)
def getall_student(db: Session=Depends(get_DB)):
    all_students = db.query(StudentModel).all()
    return all_students

@router.get('/{student_id}', response_model=StudentResponse, status_code=status.HTTP_200_OK)
def get_student(student_id: int, db: Session=Depends(get_DB)):
    student_data = db.query(StudentModel).filter(student_id==StudentModel.id).first()
    if not student_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Student with {student_id} Not Found in Student Database..')
    return student_data

@router.post('/', response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session=Depends(get_DB)):
    existing_student = db.query(StudentModel).filter(student.email == StudentModel.email).first()
    if existing_student:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Student with {existing_student.id} already Exists in Database..')
    
    new_student = StudentModel(
        name= student.name,
        email=student.email
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.put('/{student_id}', response_model=StudentResponse, status_code=status.HTTP_200_OK)
def update_student(student_id: int, student_data: StudentUpdate, db: Session=Depends(get_DB)):

    existing_student = db.query(StudentModel).filter(student_id == StudentModel.id).first()

    if not existing_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Student with {student_id} not found in Student DataBase..')
    update_student_data = student_data.model_dump(exclude_unset=True)

    for key, value in update_student_data.items():
        setattr(existing_student, key, value)

    db.commit()
    db.refresh(existing_student)
    return existing_student
    

@router.delete('/{student_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session= Depends(get_DB)):
    existing_student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not existing_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Student with {student_id} Not Found in Student Database..')
    db.delete(existing_student)
    db.commit()
    return None