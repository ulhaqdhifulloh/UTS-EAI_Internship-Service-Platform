from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import requests

app = FastAPI()

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

STUDENT_SERVICE_URL = "http://localhost:8001"
INTERNSHIP_SERVICE_URL = "http://localhost:8002"

applications = []

@app.post("/apply")
def apply(student_id: int, internship_id: int):
    student = requests.get(f"{STUDENT_SERVICE_URL}/students/{student_id}").json()
    internship = requests.get(f"{INTERNSHIP_SERVICE_URL}/internships/{internship_id}").json()

    if "error" in student or "error" in internship:
        return {"error": "Data tidak valid"}

    application = {
        "application_id": len(applications) + 1,
        "student": student,
        "internship": internship
    }
    applications.append(application)
    return application

@app.get("/applications")
def list_applications():
    return applications
