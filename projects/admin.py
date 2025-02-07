from sqladmin import ModelView
from .models import Projects

class ProjectAdmin(ModelView, model=Projects):
    column_list = [
        Projects.id, 
        Projects.title, 
        Projects.technologies, 
        Projects.description, 
        Projects.images
    ]

    column_searchable_list = [Projects.title]
    column_sortable_list = [Projects.id]

    def on_model_change(self, form, model, is_created):
        if isinstance(model.technologies, list):
            model.technologies = ",".join(model.technologies)
        if isinstance(model.images, list):
            model.images = ",".join(model.images)

    def on_model_delete(self, model):
        if model.technologies == "":
            model.technologies = None
        if model.images == "":
            model.images = None
