from sqladmin import ModelView
from .models import Experiences
import json


class ExperienceAdmin(ModelView, model=Experiences):
    name = "Experience"
    name_plural = "Experiences"
    edit_template = "custom_edit.html"
    create_template = "custom_create.html"

    column_list = [
        Experiences.id,
        Experiences.position,
        Experiences.company_name,
        Experiences.start_date,
        Experiences.end_date,
        Experiences.description,
        Experiences.technologies,
    ]

    column_searchable_list = [Experiences.position, Experiences.company_name]
    column_sortable_list = [Experiences.start_date, Experiences.end_date]

    async def on_model_get(self, model):
        if isinstance(model.technologies, str):
            try:
                model.technologies = json.loads(model.technologies)
            except json.JSONDecodeError:
                model.technologies = []
