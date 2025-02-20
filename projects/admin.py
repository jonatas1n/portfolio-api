from sqladmin import ModelView
from .models import Projects
import os

class ProjectAdmin(ModelView, model=Projects):
    edit_template = "custom_edit.html"
    create_template = "custom_create.html"

    column_list = [
        Projects.id,
        Projects.title,
        Projects.technologies,
        Projects.description,
        Projects.images,
    ]

    column_searchable_list = [Projects.title]
    column_sortable_list = [Projects.id]

    form_columns = ["title", "technologies", "description", "images"]

    async def on_model_delete(self, model):
        if model.images and os.path.exists(model.images):
            os.remove(model.images)
