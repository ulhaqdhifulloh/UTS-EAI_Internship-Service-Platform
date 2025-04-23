from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

class Student(BaseModel):
    name: str
    major: str

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    major: Optional[str] = None

students = {
    1: {"id": 1, "name": "Rina", "major": "Informatika"},
    2: {"id": 2, "name": "Doni", "major": "Sistem Informasi"}
}

@app.get("/students")
def list_students():
    return list(students.values())

@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]

@app.post("/students")
def create_student(student: Student):
    new_id = max(students.keys()) + 1 if students else 1
    students[new_id] = {"id": new_id, **student.dict()}
    return students[new_id]

@app.put("/students/{student_id}")
def update_student(student_id: int, student_update: StudentUpdate):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    
    current_student = students[student_id]
    update_data = student_update.dict(exclude_unset=True)
    current_student.update(update_data)
    students[student_id] = current_student
    
    return current_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    
    deleted_student = students[student_id]
    del students[student_id]
    return {"message": "Student deleted successfully", "deleted_student": deleted_student}
