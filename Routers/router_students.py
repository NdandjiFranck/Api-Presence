from fastapi import APIRouter,Depends, HTTPException
from typing import List
import uuid
from classes.schema import Student, StudentNoID
from database.firebase import db
from routers.router_auth import get_current_user


router= APIRouter(
    prefix='/students',
    tags=["Students"]
)

students = [
    Student(id="student1", name="Adama"),
    Student(id="student2", name="Adrien"),
    Student(id="student3", name="Akbar")
]

@router.get('', response_model=List[Student])
async def get_student():
    """List all the students from a Training Center (context fonctionnel ou technique)"""
    student_InDB =  db.child('session').get().val()
    #db.child("student").get().val()
    resultsarray= []
    if student_InDB:
        for student_id, student_info in student_InDB.items():
            student= Student( **student_info)
            resultsarray.append(student)
    return resultsarray

@router.get('/{student_id}', response_model=Student)
async def get_student_by_id(student_id: str):
    oneStudent_InDB = db.child("student").child(student_id).get().val()
    if oneStudent_InDB is None:
        raise HTTPException(status_code=404, detail="Etudient non trouvé")
    student = Student(**oneStudent_InDB)
    return student

@router.post('', response_model=Student, status_code=201)
async def add_new_student(giveName:StudentNoID):
    generatedId= uuid.uuid4()
    newStudent= Student(id=str(generatedId), name=giveName.name)
    students.append(newStudent)

    #connexion à la base de donnée
    db.child("student").child(str(generatedId)).set(newStudent.model_dump())
    return newStudent

@router.patch('/{student_id}', status_code=204)
async def modify_student_name(student_id:str, modifiedStudent: StudentNoID):
    #CONNEXION TO DATA BASE
    oneStudent_InDB = db.child("student").child(student_id).get().val()
    if oneStudent_InDB is None:
        raise HTTPException(status_code= 404, detail="Student not found")
    after_update= db.child("student").child(student_id).update({"name":modifiedStudent.name})
    return after_update

@router.delete('/{student_id}', status_code=204)
async def delete_student(student_id:str):
    oneStudent_InDB = db.child("student").child(student_id).get().val()
    if oneStudent_InDB is None:
        raise HTTPException(status_code= 404, detail="Student not found")
    after_delete= db.child("student").child(student_id).remove()
    return None