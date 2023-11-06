from pydantic import BaseModel

# Model Pydantic = Datatype
class Student(BaseModel):
    id: str
    name: str

class StudentNoID(BaseModel):
    name: str