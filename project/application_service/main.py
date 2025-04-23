from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
import httpx

app = FastAPI()

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

class Application(BaseModel):
    student_id: int
    internship_id: int

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None

applications = []

@app.post("/apply")
async def apply_internship(application: Application):
    # Verify student exists
    async with httpx.AsyncClient() as client:
        student_response = await client.get(f"http://localhost:8001/students/{application.student_id}")
        if student_response.status_code == 404:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Verify internship exists
        internship_response = await client.get(f"http://localhost:8002/internships/{application.internship_id}")
        if internship_response.status_code == 404:
            raise HTTPException(status_code=404, detail="Internship not found")
    
    # Add application
    new_application = {
        "id": len(applications) + 1,
        "student_id": application.student_id,
        "internship_id": application.internship_id,
        "status": "pending"
    }
    applications.append(new_application)
    return new_application

@app.get("/applications")
async def get_applications():
    # Enrich applications with student and internship details
    enriched_applications = []
    async with httpx.AsyncClient() as client:
        for app in applications:
            student_response = await client.get(f"http://localhost:8001/students/{app['student_id']}")
            internship_response = await client.get(f"http://localhost:8002/internships/{app['internship_id']}")
            
            enriched_app = {
                **app,
                "student": student_response.json(),
                "internship": internship_response.json()
            }
            enriched_applications.append(enriched_app)
    
    return enriched_applications

@app.put("/applications/{application_id}")
def update_application(application_id: int, application_update: ApplicationUpdate):
    # Find the application
    application = next((app for app in applications if app["id"] == application_id), None)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Update the application
    update_data = application_update.dict(exclude_unset=True)
    application.update(update_data)
    
    return application

@app.delete("/applications/{application_id}")
def delete_application(application_id: int):
    # Find the application
    application = next((app for app in applications if app["id"] == application_id), None)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Remove the application
    applications.remove(application)
    return {"message": "Application deleted successfully", "deleted_application": application}
