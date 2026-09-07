from app.database import Base, engine
from app.models import StudentModel, CourseModel, EnrollmentModel

print("Dropping All Existing Tables..")
Base.metadata.drop_all(bind=engine)

print("Recreating All Emplty Tables..")
Base.metadata.create_all(bind=engine)

print('Database Reset Completed!')