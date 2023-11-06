from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from classes.schema import Course
from database.firebase import db

router = APIRouter(
    prefix='/courses',
    tags=["Courses"]
)

courses = [
    Course(id="course1", name="Mathematics", school="School A", date_heure="2023-10-17 09:00:00"),
    Course(id="course2", name="History", school="School B", date_heure="2023-10-18 14:00:00"),
    Course(id="course3", name="Science", school="School A", date_heure="2023-10-19 10:30:00")
]

@router.get('', response_model=List[Course])
async def get_courses():
    """List all the courses."""
    return courses

@router.get('/{course_id}', response_model=Course)
async def get_course_by_id(course_id: str):
    for course in courses:
        if course.id == course_id:
            return course
    raise HTTPException(status_code=404, detail="Course not found")

@router.post('', response_model=Course, status_code=201)
async def add_new_course(new_course: Course):
    new_course.id = str(uuid.uuid4())
    courses.append(new_course)
    return new_course

@router.put('/{course_id}', response_model=Course)
async def update_course(course_id: str, updated_course: Course):
    for course in courses:
        if course.id == course_id:
            course.name = updated_course.name
            course.school = updated_course.school
            course.date_heure = updated_course.date_heure
            return course
    raise HTTPException(status_code=404, detail="Course not found")

@router.delete('/{course_id}', response_model=Course)
async def delete_course(course_id: str):
    for course in courses:
        if course.id == course_id:
            courses.remove(course)
            return course
    raise HTTPException(status_code=404, detail="Course not found")