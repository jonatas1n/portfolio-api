from fastapi import FastAPI
from admin import init_all_admins

from skills.routes import router as skills_router
from projects.routes import router as projects_router
from experiences.routes import router as experiences_router

app = FastAPI()

init_all_admins(app)

@app.get("/")
def root():
    return {"message": "It's working"}

app.include_router(skills_router)
app.include_router(projects_router)
app.include_router(experiences_router)
