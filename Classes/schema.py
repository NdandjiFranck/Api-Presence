import datetime
from pydantic import BaseModel

class Student(BaseModel):
    id: str
    name: str

class Course(BaseModel):
    id: str
    name: str
    school:str
    date_heure:str

class Attendance(BaseModel):
    id:str
    student_id:str
    course_id:str
    present: bool

class StudentNoID(BaseModel):
    name: str

class User(BaseModel):
    email: str
    password: str  