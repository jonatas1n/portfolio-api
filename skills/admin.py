from sqladmin import ModelView
from .models import Skills


class SkillAdmin(ModelView, model=Skills):
    name = "Skill"
    name_plural = "Skills"
    edit_template = "custom_edit.html"
    create_template = "custom_create.html"

    def on_model_change(self, data, model, is_created, request):
        if "title" in data:
            data["title"] = data["title"].strip()
        if "skill_type" in data:
            data["skill_type"] = data["skill_type"].strip()
        return super().on_model_change(data, model, is_created, request)

    column_list = [Skills.id, Skills.title, Skills.description]
    column_searchable_list = [Skills.title]
    column_sortable_list = [Skills.id, Skills.title]
