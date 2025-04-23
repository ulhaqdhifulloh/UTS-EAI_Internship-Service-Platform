from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

students = {
    1: {"id": 1, "name": "Rina", "major": "Informatika"},
    2: {"id": 2, "name": "Doni", "major": "Sistem Informasi"}
}

@app.get("/students/{student_id}")
def get_student(student_id: int):
    return students.get(student_id, {"error": "Mahasiswa tidak ditemukan"})
