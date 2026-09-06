from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

URL = "postgresql://postgres:2004@localhost:5432/Course_Enrollment_DB"
engine = create_engine(URL)

Base = declarative_base()

Local_Session = sessionmaker(
    bind=engine,
    autocommit = False,
    autoflush= False
)

def get_DB():
    db = Local_Session()

    try:
        yield db
    finally:
        db.close() 