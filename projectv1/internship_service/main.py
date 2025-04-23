from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

internships = {
    1: {"id": 1, "title": "Frontend Intern", "company": "Techify"},
    2: {"id": 2, "title": "Data Analyst Intern", "company": "DataLabs"}
}

@app.get("/internships")
def list_internships():
    return list(internships.values())

@app.get("/internships/{internship_id}")
def get_internship(internship_id: int):
    return internships.get(internship_id, {"error": "Lowongan tidak ditemukan"}) 