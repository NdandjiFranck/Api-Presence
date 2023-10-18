from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4
from classes.models import Student, StudentNoID
from database.firebase import db
from routers.router_auth import get_current_user


router= APIRouter(
    prefix='/students',
    tags=["Students"]
)

students = [
    Student(id="s1", name="Adama"),
    Student(id="s2", name="Adrien"),
    Student(id="ss3", name="Akbar")
]

# Verbs + Endpoints
@router.get("/", response_model=list[Student])
async def get_student(user_data: int= Depends(get_current_user)):
    queryResults = db.child('users').child(user_data['uid']).child("students").get(user_data['idToken']).val()
    if not queryResults : return []
    studentArray = [value for value in queryResults.values()]
    return studentArray

# 1. Exercice (10min) Create new Student: POST
#connecter la vraie DB (10 min)
#add oauth (10min)
# response_model permet de définir de type de réponse (ici nous retournons le student avec sont id)
# status_code est définit sur 201-Created car c'est un POST

@router.post("/", status_code=201, response_model=Student)
async def create_student(student: StudentNoID, user_data: int= Depends(get_current_user)):
    generatedId=str(uuid4())
    newStudent = Student (id=generatedId, name=student.name)
    db.child('users').child(user_data['uid']).child("students").child(generatedId).set(data=newStudent.model_dump(), token=user_data['idToken'])
    return newStudent


# 2. Exercice (10min) Student GET by ID
#connecter la vraie DB (10 min)
#add oauth (10min)
@router.get("/{student_id}", response_model=Student)
async def get_student_by_id(student_id: str, user_data: int= Depends(get_current_user)):
    queryResult = db.child('users').child(user_data['uid']).child('students').child(student_id).get(user_data['idToken']).val()
    if not queryResult : raise HTTPException(status_code=404, detail="Student not found") 
    return queryResult

# 3. Exercice (10min) PATCH Student (name)
#connecter la vraie DB (10 min)
#add oauth (10min)
@router.patch("/{student_id}", response_model=Student)
async def student_update(student_id: str, student: StudentNoID, user_data: int= Depends(get_current_user)):
    queryResult = db.child('users').child(user_data['uid']).child('students').child(student_id).get(user_data['idToken']).val()
    if not queryResult : raise HTTPException(status_code=404, detail="Student not found") 
    updatedStudent = Student(id=student_id, **student.model_dump())
    return db.child('users').child(user_data['uid']).child('students').child(student_id).update(data=updatedStudent.model_dump(), token=user_data['idToken'])

# 4. Exercice (10min) DELETE Student
#connecter la vraie DB (10 min)
#add oauth (10min)
@router.delete("/{student_id}", status_code=202, response_model=str)
async def student_delete(student_id: str, user_data: int= Depends(get_current_user)) :
    queryResult = db.child('users').child(user_data['uid']).child('students').child(student_id).get(user_data['idToken']).val()
    if not queryResult : 
        raise HTTPException(status_code=404, detail="Student not found")
    db.child('users').child(user_data['uid']).child('students').child(student_id).remove(token=user_data['idToken'])
    return "Student deleted"


#'Students' auront des 'Attendances' pour des 'Sessions'
# utilisateurs, lien vers une ressource
# API vendu à des centre de formations ... 'Center' -> Sessions + Students -> Attendences
