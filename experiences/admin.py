from sqladmin import ModelView
from .models import Experiences

class ExperienceAdmin(ModelView, model=Experiences):
    column_list = [
        Experiences.id, 
        Experiences.title, 
        Experiences.company_name, 
        Experiences.start_date, 
        Experiences.end_date, 
        Experiences.description, 
        Experiences.technologies
    ]
    
    column_searchable_list = [Experiences.title, Experiences.company_name]
    column_sortable_list = [Experiences.start_date, Experiences.end_date]

    def on_model_change(self, form, model, is_created):
        if isinstance(model.technologies, list):
            model.technologies = ",".join(model.technologies)

    def on_model_delete(self, model):
        if model.technologies == "":
            model.technologies = None
