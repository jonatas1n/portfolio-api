from fastapi import FastAPI
from sqladmin import Admin
from database.db import engine
from skills.admin import SkillAdmin
from experiences.admin import ExperienceAdmin
from projects.admin import ProjectAdmin

admin = None

def init_all_admins(app: FastAPI):
    global admin
    if admin is None:
        admin = Admin(app, engine)
    
    admin.add_view(SkillAdmin)
    admin.add_view(ExperienceAdmin)
    admin.add_view(ProjectAdmin)
