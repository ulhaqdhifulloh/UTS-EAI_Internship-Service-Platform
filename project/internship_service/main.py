from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

class Internship(BaseModel):
    title: str
    company: str

class InternshipUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None

internships = {
    1: {"id": 1, "title": "Frontend Intern", "company": "Techify"},
    2: {"id": 2, "title": "Data Analyst Intern", "company": "DataLabs"}
}

@app.get("/internships")
def list_internships():
    return list(internships.values())

@app.get("/internships/{internship_id}")
def get_internship(internship_id: int):
    if internship_id not in internships:
        raise HTTPException(status_code=404, detail="Internship not found")
    return internships[internship_id]

@app.post("/internships")
def create_internship(internship: Internship):
    new_id = max(internships.keys()) + 1 if internships else 1
    internships[new_id] = {"id": new_id, **internship.dict()}
    return internships[new_id]

@app.put("/internships/{internship_id}")
def update_internship(internship_id: int, internship_update: InternshipUpdate):
    if internship_id not in internships:
        raise HTTPException(status_code=404, detail="Internship not found")
    
    current_internship = internships[internship_id]
    update_data = internship_update.dict(exclude_unset=True)
    current_internship.update(update_data)
    internships[internship_id] = current_internship
    
    return current_internship

@app.delete("/internships/{internship_id}")
def delete_internship(internship_id: int):
    if internship_id not in internships:
        raise HTTPException(status_code=404, detail="Internship not found")
    
    deleted_internship = internships[internship_id]
    del internships[internship_id]
    return {"message": "Internship deleted successfully", "deleted_internship": deleted_internship} 